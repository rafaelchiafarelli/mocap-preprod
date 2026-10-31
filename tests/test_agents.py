"""What the agent definitions promise about the film root (preprod-link agents/*)."""

from pathlib import Path

import pytest

AGENTS = sorted((Path(__file__).resolve().parent.parent / ".claude" / "agents").glob("*.md"))


@pytest.mark.parametrize("agent", AGENTS, ids=lambda p: p.stem)
def test_reads_the_film_root_the_writer_keeps(agent):
    text = agent.read_text(encoding="utf-8")
    for needle in ("film.json", "bible/scene-index.json", "script.fountain", "mocap-contracts"):
        assert needle in text, needle
    assert "word/document.xml" not in text
