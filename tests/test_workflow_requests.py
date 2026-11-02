"""preprod-link workflow-tool/3: send_request, my_requests and answer_request, on a test database."""

import json

import mocap_contracts as mc
import pytest
from mcp_client import AGENT, answer, call, register, text
from mocap_contracts import db

OTHER = "sound-design-planner"
MEMO = "analysis/work/props-continuity.md"


@pytest.fixture
def two_agents(film_root):
    register(film_root, OTHER, "sound")
    return film_root


def _send(root, **kw):
    args = {"agent": AGENT, "to": OTHER, "items": ["prop-w-1"], "scenes": ["1", "2"],
            "what": "Does the cup ring when it lands?", "source": MEMO} | kw
    return call(root, "send_request", **args)


def _answer(root, **kw):
    args = {"agent": OTHER, "id": "request-props-1", "status": "done", "answer": "sound-design.md, scene 1."} | kw
    return call(root, "answer_request", **args)


def _stored(root):
    with db.open(root / "workflow.sqlite") as d:
        return d.requests.list()


def _refused(result, reason):
    assert result.is_error
    assert reason in text(result)


def test_a_round_trip_between_two_agents(two_agents):
    assert answer(_send(two_agents)) == {"id": "request-props-1"}

    mine = answer(call(two_agents, "my_requests", agent=OTHER))
    assert mine["answers"] == []
    [got] = mine["to_me"]
    assert (got["id"], got["from"], got["to"], got["status"]) == ("request-props-1", AGENT, OTHER, "open")
    assert (got["items"], got["scenes"], got["source"]) == (["prop-w-1"], ["1", "2"], MEMO)
    assert got["answer"] is None
    assert answer(call(two_agents, "my_requests", agent=AGENT)) == {"to_me": [], "answers": []}

    assert answer(_answer(two_agents)) == {"id": "request-props-1", "status": "done"}

    assert answer(call(two_agents, "my_requests", agent=OTHER)) == {"to_me": [], "answers": []}
    theirs = answer(call(two_agents, "my_requests", agent=AGENT))
    assert theirs["to_me"] == []
    [done] = theirs["answers"]
    assert (done["status"], done["answer"], done["answered_by"]) == ("done", "sound-design.md, scene 1.", OTHER)


def test_a_stored_request_holds_to_the_contract(two_agents):
    answer(_send(two_agents))
    [r] = _stored(two_agents)
    assert mc.to_json(r)
    assert getattr(r, "from") == AGENT and r.time.endswith("Z")
    assert mc.RequestStatus.Name(r.status) == "REQUEST_STATUS_OPEN"
    assert not r.HasField("answer") and not r.HasField("answered_by")


def test_a_declined_request_says_why(two_agents):
    answer(_send(two_agents))
    assert answer(_answer(two_agents, status="declined", answer="Not sound."))["status"] == "declined"
    [done] = answer(call(two_agents, "my_requests", agent=AGENT))["answers"]
    assert (done["status"], done["answer"]) == ("declined", "Not sound.")


@pytest.mark.parametrize("who", [AGENT, "visual-development-analyst"])
def test_answer_refused_to_anyone_but_the_recipient(two_agents, who):
    register(two_agents, "visual-development-analyst", "visdev")
    answer(_send(two_agents))
    _refused(_answer(two_agents, agent=who), "only its recipient may answer it")
    assert not _stored(two_agents)[0].HasField("answer")


def test_answer_refused_to_an_unregistered_agent(two_agents):
    answer(_send(two_agents))
    _refused(_answer(two_agents, agent="nobody"), "has no space in film.json")


def test_a_request_to_the_creator_is_not_answered_here(two_agents):
    answer(_send(two_agents, to="creator"))
    _refused(_answer(two_agents, agent=OTHER), "addressed to 'creator'")
    assert answer(call(two_agents, "my_requests", agent=OTHER))["to_me"] == []
    assert not _stored(two_agents)[0].HasField("answer")


def test_answer_refused_twice(two_agents):
    answer(_send(two_agents))
    answer(_answer(two_agents))
    _refused(_answer(two_agents, status="declined", answer="Changed my mind."), "already answered")
    assert _stored(two_agents)[0].answer == "sound-design.md, scene 1."


@pytest.mark.parametrize("kw,reason", [
    ({"status": "open"}, "status must be done or declined"),
    ({"status": "DONE"}, "status must be done or declined"),
    ({"answer": "  "}, "answer is empty"),
    ({"id": "request-props-9"}, "no request"),
])
def test_answer_refused_when_broken(two_agents, kw, reason):
    answer(_send(two_agents))
    _refused(_answer(two_agents, **kw), reason)
    assert not _stored(two_agents)[0].HasField("answer")


def test_send_refused_to_someone_unregistered(two_agents):
    _refused(_send(two_agents, to="nobody"), "neither 'creator' nor a registered agent")
    _refused(_send(two_agents, to="writer"), "neither 'creator' nor a registered agent")
    assert _stored(two_agents) == []


def test_send_refused_to_an_unregistered_sender(two_agents):
    _refused(_send(two_agents, agent="nobody"), "has no space in film.json")


@pytest.mark.parametrize("kw,reason", [
    ({"to": AGENT}, "can't be the sender"),
    ({"what": " "}, "what is empty"),
    ({"items": ["cup"]}, "items must be record ids"),
    ({"scenes": ["1a"]}, "scenes must be scene numbers"),
    ({"source": "/home/me/memo.md"}, "source"),
])
def test_send_refused_by_the_contract_rules(two_agents, kw, reason):
    _refused(_send(two_agents, **kw), reason)
    assert _stored(two_agents) == []


def test_items_and_scenes_may_be_empty(two_agents):
    # a missing item has no id yet: the request says it in `what`
    answer(_send(two_agents, to="creator", items=[], scenes=[], what="Please add a kettle to the bible."))
    assert list(_stored(two_agents)[0].items) == []


def test_requests_and_proposals_share_the_spaces_counters(two_agents):
    answer(_send(two_agents))
    answer(_send(two_agents))
    answer(call(two_agents, "propose", agent=AGENT, item="prop-w-1", field="look.shape", value="tall", source=MEMO))
    counters = json.loads((two_agents / "ids" / "props.json").read_text())
    assert counters == {"next": {"proposal": 2, "request": 3}}
