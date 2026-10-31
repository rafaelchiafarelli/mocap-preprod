"""The neutral fixture film root (tests/fixtures/film/) reads and holds together."""

import hashlib
import re
from pathlib import Path

import mocap_contracts as mc

FILM = Path(__file__).resolve().parent / "fixtures" / "film"
AGENTS = Path(__file__).resolve().parent.parent / ".claude" / "agents"


def read(cls, rel):
    return mc.from_json(cls, (FILM / rel).read_text(encoding="utf-8"))


def bible_items():
    return {p: mc.from_json(mc.BibleItem, p.read_text(encoding="utf-8"))
            for p in (FILM / "bible").glob("*/**/item.json")}


def test_every_record_reads():
    film = read(mc.Film, "film.json")
    assert {p.name for p in film.parts} >= {"script", "bible", "annotations", "history"}
    for p in (FILM / "ids").glob("*.json"):
        mc.from_json(mc.IdCounters, p.read_text(encoding="utf-8"))
    assert len(bible_items()) == 8
    read(mc.SceneIndex, "bible/scene-index.json")
    changes = sorted((FILM / "bible" / "sync").glob("*-changes.json"))
    assert len(changes) == 2
    for p in changes:
        mc.from_json(mc.ChangeSet, p.read_text(encoding="utf-8"))
    for p in (FILM / "annotations").glob("annotation-*.json"):
        mc.from_json(mc.Annotation, p.read_text(encoding="utf-8"))
    read(mc.ShotCounters, "annotations/shot-counters.json")
    read(mc.FrontMatter, "settings/front-matter.json")
    for line in (FILM / "history").glob("*.jsonl"):
        for text in line.read_text(encoding="utf-8").splitlines():
            mc.from_json(mc.Change, text)


def test_scene_numbers_and_ids_resolve():
    index = read(mc.SceneIndex, "bible/scene-index.json")
    scenes = {s.scene for s in index.scenes}
    script = (FILM / "script.fountain").read_text(encoding="utf-8")
    assert scenes == set(re.findall(r"#([0-9]+(?:\.[A-Z])?)#", script))

    items = {i.id: i for i in bible_items().values()}
    for s in index.scenes:
        assert not s.set_id or s.set_id in items
        assert all(c.id in items for c in s.characters if c.id)
        assert all(p.id in items for p in s.props if p.id)
    for i in items.values():
        assert all(link.scene in scenes for link in i.links)
        assert all(link.item in items for link in i.links if link.item)
    for p in (FILM / "annotations").glob("annotation-*.json"):
        assert mc.from_json(mc.Annotation, p.read_text(encoding="utf-8")).anchor.scene in scenes

    # a change set's to_hash is the sha256 of the scene-index.json it made: the
    # latest one matches the accepted index
    latest = sorted((FILM / "bible" / "sync").glob("*-changes.json"))[-1]
    index_hash = hashlib.sha256((FILM / "bible" / "scene-index.json").read_bytes()).hexdigest()
    assert mc.from_json(mc.ChangeSet, latest.read_text(encoding="utf-8")).to_hash == index_hash


def test_worklist_assigns_registered_agents():
    names = {re.search(r"^\*\*Display name:\*\* (.+)$", p.read_text(encoding="utf-8"), re.M).group(1)
             for p in AGENTS.glob("*.md")}
    rows = [line.split("|") for line in
            (FILM / "analysis" / "production-worklist.md").read_text(encoding="utf-8").splitlines()
            if re.match(r"^\| [A-Z]+-\d+ ", line)]
    assert rows and all(r[5].strip() in names for r in rows)
