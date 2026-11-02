"""preprod-link workflow-tool/2: propose and my_proposals, on a test database."""

import json

import mocap_contracts as mc
import pytest
from mcp_client import AGENT, answer, call, register, session, text
from mocap_contracts import db

ITEM = "prop-w-1"
MEMO = "analysis/work/props-continuity.md"


def _propose(root, **kw):
    args = {"agent": AGENT, "item": ITEM, "field": "look.shape", "value": "tall", "source": MEMO} | kw
    return call(root, "propose", **args)


def _review(root, proposal, outcome, **kw):
    with db.open(root / "workflow.sqlite") as d:
        d.reviews.create(mc.Review(proposal=proposal, by="creator", time="2026-11-02T10:00:00Z",
                                   outcome=mc.ReviewOutcome.Value(f"REVIEW_OUTCOME_{outcome}"), **kw))


def _proposals(root):
    with db.open(root / "workflow.sqlite") as d:
        return d.proposals.list()


def _refused(result, reason):
    assert result.is_error
    assert reason in text(result)


def test_propose_writes_one_proposal(film_root):
    assert answer(_propose(film_root, note="It has to read from far.",
                           change_set="20261031T130000Z-changes.json")) == {"id": "proposal-props-1"}
    [p] = _proposals(film_root)
    assert (p.id, p.item, p.change_set) == ("proposal-props-1", ITEM, "20261031T130000Z-changes.json")
    assert (p.value.field, p.value.text, p.value.note) == ("look.shape", "tall", "It has to read from far.")
    assert mc.ValueState.Name(p.value.state) == "VALUE_STATE_PROPOSAL"
    assert (p.value.by, p.value.source, p.value.department) == (AGENT, MEMO, "props")
    assert mc.to_json(p)  # holds to the contract's rules
    assert p.time.endswith("Z")


def test_optional_arguments_stay_absent(film_root):
    answer(_propose(film_root))
    [p] = _proposals(film_root)
    assert not p.HasField("change_set")
    assert not p.value.HasField("note") and not p.value.HasField("scene")


def test_ids_count_up_and_the_counter_is_kept(film_root):
    assert answer(_propose(film_root))["id"] == "proposal-props-1"
    assert answer(_propose(film_root, value="squat"))["id"] == "proposal-props-2"
    counters = json.loads((film_root / "ids" / "props.json").read_text())
    assert counters == {"next": {"proposal": 3}}


def test_the_counter_keeps_other_kinds_and_its_number(film_root):
    (film_root / "ids" / "props.json").write_text(mc.to_json(mc.IdCounters(next={"proposal": 7, "annotation": 2})))
    assert answer(_propose(film_root))["id"] == "proposal-props-7"
    assert json.loads((film_root / "ids" / "props.json").read_text()) == {"next": {"annotation": 2, "proposal": 8}}


def test_a_counter_left_behind_by_a_crash_is_passed(film_root):
    answer(_propose(film_root))
    (film_root / "ids" / "props.json").unlink()
    assert answer(_propose(film_root, value="squat"))["id"] == "proposal-props-2"


def test_a_number_takes_the_catalogs_unit(film_root):
    answer(_propose(film_root, field="look.height", value="0.12"))
    [p] = _proposals(film_root)
    assert (p.value.number, p.value.unit) == ("0.12", "m")
    assert not p.value.HasField("text")


def test_a_per_scene_field_takes_its_scene(film_root):
    answer(_propose(film_root, field="state.state", value="full", scene="1"))
    assert _proposals(film_root)[0].value.scene == "1"


@pytest.mark.parametrize("item", ["prop-w-99", "annotation-w-1", "cup", ""])
def test_refused_when_the_item_is_not_in_the_bible(film_root, item):
    _refused(_propose(film_root, item=item), "no bible item")
    assert _proposals(film_root) == []


def test_refused_outside_the_agents_departments(film_root):
    # a prop's capture group is nobody's
    _refused(_propose(film_root, field="capture.stand_in"), "outside what props-continuity-planner proposes for")
    assert _proposals(film_root) == []


def test_the_owner_of_another_department_may_propose_it(film_root):
    register(film_root, "story-editorial-analyst", "story")
    fields = {k: f for k, f in mc.bible.fields("character").items() if f.department == "story" and f.type == "text"
              and not f.per_scene}
    field = next(iter(fields))
    assert answer(call(film_root, "propose", agent="story-editorial-analyst", item="character-w-1", field=field,
                       value="wants out", source=MEMO))["id"] == "proposal-story-1"


def test_refused_to_an_agent_that_proposes_nothing(film_root):
    register(film_root, "cinematography-planner", "cine")
    _refused(call(film_root, "propose", agent="cinematography-planner", item=ITEM, field="look.shape",
                  value="tall", source=MEMO), "outside what cinematography-planner proposes for")


def test_refused_to_an_unregistered_agent(film_root):
    _refused(_propose(film_root, agent="sound-design-planner"), "has no space in film.json")
    _refused(call(film_root, "my_proposals", agent="sound-design-planner"), "has no space in film.json")


def test_refused_when_the_field_is_not_in_the_catalog(film_root):
    _refused(_propose(film_root, field="look.mood"), "not a prop field of the catalog")


def test_refused_by_the_contract_rules(film_root):
    _refused(_propose(film_root, source="/home/me/memo.md"), "source")
    _refused(_propose(film_root, field="look.shape", scene="1"), "not per scene")
    _refused(_propose(film_root, field="look.height", value="tall"), "decimal")
    _refused(_propose(film_root, change_set="bible/sync/a.json"), "change_set")
    _refused(_propose(film_root, value="  "), "value is empty")
    assert _proposals(film_root) == []


def test_a_refused_proposal_takes_no_number(film_root):
    _refused(_propose(film_root, source="/home/me/memo.md"), "source")
    assert answer(_propose(film_root))["id"] == "proposal-props-1"


def test_refused_when_the_same_value_was_rejected(film_root):
    answer(_propose(film_root))
    _review(film_root, "proposal-props-1", "REJECTED")
    _refused(_propose(film_root), "already rejected this value in proposal-props-1")
    assert len(_proposals(film_root)) == 1


def test_a_rejection_only_covers_that_item_field_scene_and_value(film_root):
    answer(_propose(film_root, field="state.state", value="full", scene="1"))
    _review(film_root, "proposal-props-1", "REJECTED")
    answer(_propose(film_root, field="state.state", value="empty", scene="1"))
    answer(_propose(film_root, field="state.state", value="full", scene="2"))
    answer(_propose(film_root, field="state.state", value="full", scene="1", item="prop-w-2"))
    assert len(_proposals(film_root)) == 4


def test_only_a_rejection_stops_it(film_root):
    answer(_propose(film_root))
    _review(film_root, "proposal-props-1", "APPROVED")
    answer(_propose(film_root))


def test_another_agents_rejected_value_is_refused_too(film_root):
    register(film_root, "visual-development-analyst", "visdev")
    answer(call(film_root, "propose", agent="visual-development-analyst", item="set-w-1",
                field=_art_field(), value="warm", source=MEMO))
    _review(film_root, "proposal-visdev-1", "REJECTED")
    _refused(call(film_root, "propose", agent="visual-development-analyst", item="set-w-1",
                  field=_art_field(), value="warm", source=MEMO), "already rejected")


def _art_field():
    return next(k for k, f in mc.bible.fields("set").items()
                if f.department == "art" and f.type == "text" and not f.per_scene)


def test_my_proposals_lists_them_with_their_reviews(film_root):
    answer(_propose(film_root))
    answer(_propose(film_root, value="squat"))
    answer(_propose(film_root, value="round"))
    _review(film_root, "proposal-props-1", "EDITED", note="Shorter.", text="short")
    _review(film_root, "proposal-props-2", "REJECTED", note="No.")
    rows = answer(call(film_root, "my_proposals", agent=AGENT))
    assert [r["id"] for r in rows] == ["proposal-props-1", "proposal-props-2", "proposal-props-3"]
    assert rows[0]["review"]["outcome"] == "edited"
    assert (rows[0]["review"]["note"], rows[0]["review"]["text"]) == ("Shorter.", "short")
    assert (rows[1]["review"]["outcome"], rows[1]["review"]["text"]) == ("rejected", None)
    assert rows[2]["review"] is None
    assert (rows[0]["value"], rows[0]["field"], rows[0]["item"]) == ("tall", "look.shape", ITEM)


def test_my_proposals_open_only(film_root):
    answer(_propose(film_root))
    answer(_propose(film_root, value="squat"))
    _review(film_root, "proposal-props-1", "APPROVED")
    rows = answer(call(film_root, "my_proposals", agent=AGENT, open_only=True))
    assert [r["id"] for r in rows] == ["proposal-props-2"]


def test_my_proposals_shows_only_the_callers(film_root):
    register(film_root, "visual-development-analyst", "visdev")
    answer(_propose(film_root))
    assert answer(call(film_root, "my_proposals", agent="visual-development-analyst")) == []


def test_never_touches_the_bible(film_root):
    before = {p: p.read_bytes() for p in (film_root / "bible").rglob("*") if p.is_file()}
    answer(_propose(film_root))
    assert before == {p: p.read_bytes() for p in (film_root / "bible").rglob("*") if p.is_file()}


def test_tools_of_this_task_are_listed(film_root):
    async def tools(s):
        return {t.name for t in (await s.list_tools()).tools}
    assert {"film_spaces", "propose", "my_proposals"} <= session(film_root, tools)
