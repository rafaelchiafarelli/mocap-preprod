"""What the agent definitions promise about the film root (preprod-link agents/*)."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
AGENTS = sorted((ROOT / ".claude" / "agents").glob("*.md"))


@pytest.mark.parametrize("agent", AGENTS, ids=lambda p: p.stem)
def test_reads_the_film_root_the_writer_keeps(agent):
    text = agent.read_text(encoding="utf-8")
    for needle in ("film.json", "bible/scene-index.json", "mocap-contracts"):
        assert needle in text, needle
    # the facilitator works from the readiness report, the bible and the front
    # matter; every other agent quotes the script
    if agent.stem != "pre-production-decision-facilitator":
        assert "script.fountain" in text
    assert "word/document.xml" not in text


SPECIALISTS = [p for p in AGENTS if p.stem not in
               ("script-readiness-analyst", "pre-production-decision-facilitator")]
HEADER = re.compile(
    r"^Covers: scenes (?P<scenes>none|[0-9A-Z., ]+); items (?P<items>none|[a-z0-9, -]+)\n"
    r"Change set: (?P<changes>none|bible/sync/\S+-changes\.json)\n"
    r"Not revisited: scenes (none|[0-9A-Z., ]+); items (none|[a-z0-9, -]+)$",
    re.M,
)


@pytest.mark.parametrize("agent", SPECIALISTS, ids=lambda p: p.stem)
def test_specialists_keep_the_change_set_header(agent):
    text = agent.read_text(encoding="utf-8")
    assert "## Change-set runs" in text
    for line in ("Covers: scenes", "Change set:", "Not revisited: scenes"):
        assert line in text
    assert "Start with the change-set header" in text


def test_the_documented_header_example_parses_and_resolves():
    process = (ROOT / "preprod.process.md").read_text(encoding="utf-8")
    m = HEADER.search(process)
    assert m, "no header example in preprod.process.md"

    import mocap_contracts as mc
    film = ROOT / "tests" / "fixtures" / "film"
    index = mc.from_json(mc.SceneIndex, (film / "bible" / "scene-index.json").read_text())
    scenes = {s.scene for s in index.scenes}
    assert set(m["scenes"].split(", ")) <= scenes
    assert (film / m["changes"]).exists()


@pytest.mark.parametrize("agent", AGENTS, ids=lambda p: p.stem)
def test_no_agent_writes_prompts_for_another(agent):
    text = agent.read_text(encoding="utf-8").lower()
    assert "suggested prompt" not in text and "copyable prompt" not in text


@pytest.mark.parametrize("stem", ["script-readiness-analyst", "pre-production-decision-facilitator"])
def test_stages_hand_over_with_a_plain_next_line(stem):
    assert "`Next: " in (ROOT / ".claude" / "agents" / f"{stem}.md").read_text(encoding="utf-8")
