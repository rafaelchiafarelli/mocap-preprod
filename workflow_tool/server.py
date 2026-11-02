"""The tools the agents call, on one film root.

`film.json` is read on every call, so a space the writer registers while an
agent runs is seen. The database is opened per use and never held: the writer
works on the same file, and one program writes at a time.
"""

from __future__ import annotations

from pathlib import Path

import mocap_contracts as mc
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mocap_contracts import ContractError, db, film


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


def workflow_path(root: Path, record: mc.Film) -> Path:
    for part in record.parts:
        if part.name == film.WORKFLOW_PART:
            return root / part.path
    raise FilmError(f"{root / film.FILM_FILE} has no {film.WORKFLOW_PART!r} part")


def open_database(root: Path) -> db.Database:
    return db.open(workflow_path(root, read_film(root)))


def agent_spaces(record: mc.Film) -> dict[str, str]:
    """Each agent's space code. The writer owns a space too, but is no agent."""
    return {s.owner: s.code for s in record.spaces if s.owner != film.WRITER}


def check_agent(record: mc.Film, agent: str) -> str:
    """The calling agent's space code. Refuses a name with no space in film.json."""
    spaces = agent_spaces(record)
    if agent not in spaces:
        raise FilmError(f"agent {agent!r} has no space in film.json; registered: {sorted(spaces)}")
    return spaces[agent]


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

    return server
