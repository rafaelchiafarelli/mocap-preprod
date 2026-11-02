"""The tools the agents call, on one film root.

`film.json` is read on every call, so a space the writer registers while an
agent runs is seen. The database is opened per use and never held: the writer
works on the same file, and one program writes at a time.
"""

from __future__ import annotations

import datetime
import json
import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import mocap_contracts as mc
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mocap_contracts import ContractError, bible, db, film

# The catalog departments each agent may propose for (preprod-link agents/3).
# No other agent proposes, and nobody covers `capture`.
DEPARTMENTS = {
    "visual-development-analyst": ("art", "lighting"),
    "character-design-planner": ("character-design", "wardrobe", "hair-makeup"),
    "props-continuity-planner": ("props",),
    "sound-design-planner": ("sound",),
    "story-editorial-analyst": ("story",),
}


class FilmError(ToolError):
    """This film root can't be served, or the caller isn't one of its agents.

    A ToolError, the one exception whose text the SDK passes on to the agent.
    """


def read_film(root: Path) -> mc.Film:
    path = root / film.FILM_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise FilmError(f"can't read {path}: {e.strerror}") from None
    try:
        return mc.from_json(mc.Film, text)
    except ContractError as e:
        raise FilmError(f"{path}: {e}") from None


def part_path(root: Path, record: mc.Film, name: str) -> Path:
    for part in record.parts:
        if part.name == name:
            return root / part.path
    raise FilmError(f"{root / film.FILM_FILE} has no {name!r} part")


def open_database(root: Path) -> db.Database:
    return db.open(part_path(root, read_film(root), film.WORKFLOW_PART))


@contextmanager
def database(root: Path, record: mc.Film) -> Iterator[db.Database]:
    """The database for one call; a record the contract refuses is told to the agent."""
    try:
        with db.open(part_path(root, record, film.WORKFLOW_PART)) as d:
            yield d
    except ContractError as e:
        raise FilmError(str(e)) from None


def agent_spaces(record: mc.Film) -> dict[str, str]:
    """Each agent's space code. The writer owns a space too, but is no agent."""
    return {s.owner: s.code for s in record.spaces if s.owner != film.WRITER}


def check_agent(record: mc.Film, agent: str) -> str:
    """The calling agent's space code. Refuses a name with no space in film.json."""
    spaces = agent_spaces(record)
    if agent not in spaces:
        raise FilmError(f"agent {agent!r} has no space in film.json; registered: {sorted(spaces)}")
    return spaces[agent]


def has_item(root: Path, record: mc.Film, item: str) -> bool:
    """Whether a bible item with this id exists. Items are found by id: a folder is named by its item's name."""
    map_ = bible.map_of(item)
    if map_ is None:
        return False
    folder = part_path(root, record, "bible") / bible.MAP_FOLDERS[map_]
    for path in folder.rglob(bible.ITEM_FILE):
        try:
            if json.loads(path.read_text(encoding="utf-8")).get("id") == item:
                return True
        except ValueError:
            continue  # the writer's to fix; it doesn't hide the other items
    return False


def new_id(root: Path, code: str, kind: str, table: db.Table) -> tuple[str, int]:
    """The next free id of this space and the number it took. Passes a number a
    record already holds, which a crash between the record and its counter can leave."""
    path = root / film.ids_file(code)
    n = mc.from_json(mc.IdCounters, path.read_text(encoding="utf-8")).next.get(kind, 1) if path.exists() else 1
    while table.read(film.record_id(kind, code, n)) is not None:
        n += 1
    return film.record_id(kind, code, n), n


def save_counter(root: Path, code: str, kind: str, n: int) -> None:
    """Record that `n` is taken, keeping the space's other counters."""
    path = root / film.ids_file(code)
    counters = mc.from_json(mc.IdCounters, path.read_text(encoding="utf-8")) if path.exists() else mc.IdCounters()
    counters.next[kind] = n + 1
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(mc.to_json(counters), encoding="utf-8")
    os.replace(temp, path)


def now() -> str:
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def proposed_value(item: str, field: str, value: str, scene: str | None, note: str | None,
                   source: str, agent: str) -> mc.BibleValue:
    """A proposal's value, with its department and unit from the catalog."""
    map_ = bible.map_of(item)
    known = bible.fields(map_).get(field)
    if known is None:
        raise FilmError(f"{field!r} is not a {map_} field of the catalog")
    if known.department not in DEPARTMENTS.get(agent, ()):
        raise FilmError(f"{field} belongs to the department {known.department!r}, outside what "
                        f"{agent} proposes for: {list(DEPARTMENTS.get(agent, ()))}")
    if not value.strip():
        raise FilmError("value is empty")
    v = mc.BibleValue(field=field, state=mc.ValueState.Value("VALUE_STATE_PROPOSAL"), source=source,
                      department=known.department, by=agent)
    if known.type == "number":
        v.number, v.unit = value, known.unit
    else:
        v.text = value
    if scene is not None:
        v.scene = scene
    if note is not None:
        v.note = note
    return v


def said(v: mc.BibleValue) -> str:
    return v.number if v.HasField("number") else v.text


def was_rejected(d: db.Database, item: str, v: mc.BibleValue) -> str | None:
    """The id of an earlier proposal of this item, field, scene and value that was rejected."""
    scene = v.scene if v.HasField("scene") else None
    rejected = mc.ReviewOutcome.Value("REVIEW_OUTCOME_REJECTED")
    for p in d.proposals.list():
        if (p.item, p.value.field, said(p.value)) == (item, v.field, said(v)) \
                and (p.value.scene if p.value.HasField("scene") else None) == scene:
            review = d.reviews.read(p.id)
            if review is not None and review.outcome == rejected:
                return p.id
    return None


def optional(msg: Any, field: str) -> str | None:
    return getattr(msg, field) if msg.HasField(field) else None


def proposal_row(p: mc.Proposal, review: mc.Review | None) -> dict[str, Any]:
    return {
        "id": p.id, "item": p.item, "field": p.value.field, "scene": optional(p.value, "scene"),
        "value": said(p.value), "unit": optional(p.value, "unit"), "note": optional(p.value, "note"),
        "source": p.value.source, "time": p.time, "change_set": optional(p, "change_set"),
        "review": None if review is None else {
            "outcome": mc.ReviewOutcome.Name(review.outcome).removeprefix("REVIEW_OUTCOME_").lower(),
            "note": optional(review, "note"), "text": optional(review, "text"), "time": review.time,
        },
    }


def make_server(root: Path) -> MCPServer:
    server = MCPServer("workflow")

    @server.tool()
    def film_spaces(agent: str) -> list[dict[str, str]]:
        """The agents registered on this film and their id space codes.

        agent: your own agent name, as in your file's frontmatter.
        """
        record = read_film(root)
        check_agent(record, agent)
        return [{"agent": a, "space": c} for a, c in agent_spaces(record).items()]

    @server.tool()
    def propose(agent: str, item: str, field: str, value: str, source: str, scene: str | None = None,
                note: str | None = None, change_set: str | None = None) -> dict[str, str]:
        """Propose a value for one field of an existing bible item, for the creator to decide.

        agent: your own agent name.
        item: the bible item's id, e.g. prop-w-1. It must exist: to ask for a
            missing item or scene link, send a request to the creator.
        field: the catalog field, <group>.<field>, in a department you propose for.
        value: the value as text; for a number field a decimal in the catalog's unit.
        source: your memo's path, relative to the film root.
        scene: the scene number, on a per-scene field only.
        note: why, in one line.
        change_set: the bible/sync/ file name this run answers, on a change-set run.

        Refused when a proposal of the same item, field, scene and value was
        already rejected. Returns the new proposal's id.
        """
        record = read_film(root)
        code = check_agent(record, agent)
        if not has_item(root, record, item):
            raise FilmError(f"no bible item {item!r}: send a request to the creator instead")
        v = proposed_value(item, field, value, scene, note, source, agent)
        with database(root, record) as d:
            if rejected := was_rejected(d, item, v):
                raise FilmError(f"the creator already rejected this value in {rejected}: don't propose it again")
            rid, n = new_id(root, code, "proposal", d.proposals)
            proposal = mc.Proposal(id=rid, item=item, value=v, time=now())
            if change_set is not None:
                proposal.change_set = change_set
            d.proposals.create(proposal)
            save_counter(root, code, "proposal", n)
        return {"id": rid}

    @server.tool()
    def my_proposals(agent: str, open_only: bool = False) -> list[dict[str, Any]]:
        """Your proposals with the creator's review of each: outcome, note, edited text.

        Read this before proposing: a rejected value is not proposed again.

        agent: your own agent name.
        open_only: only the ones not reviewed yet.
        """
        record = read_film(root)
        check_agent(record, agent)
        with database(root, record) as d:
            reviews = {r.proposal: r for r in d.reviews.list()}
            return [proposal_row(p, reviews.get(p.id)) for p in d.proposals.list()
                    if p.value.by == agent and not (open_only and p.id in reviews)]

    return server
