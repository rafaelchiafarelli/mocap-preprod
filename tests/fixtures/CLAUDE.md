# tests/fixtures — test data

**Role:** a neutral film root the tests (and later the agents' tool) run
against. No film material.

**Entry points:** — (read by `tests/`; rebuilt by
`tools/make_fixture_film.sh`).

**Inputs → Outputs:** mocap-writer's own code → `film/` (everything but
`film/analysis/`, which is hand-written).

## Files

- `film/` — THE BLUE CUP, a neutral three-draft-scene short:
  - `film.json`, `ids/w.json`, `script.fountain` (scenes `1`, `2`, `2.A`,
    `3`), `settings/front-matter.json` (title, logline), `history/`.
  - `bible/` — sets Kitchen, Street; characters Ana, Marco; props Blue
    Cup, Letter, Umbrella; wardrobe Raincoat (worn by Ana in scene 2).
    Values in states `script-stated`, `creator-approved` and `tbd`.
  - `bible/scene-index.json` and `bible/sync/`: two accepted syncs, the
    first with every scene added, the second with scene `2.A` added,
    scene `3` changed and the prop word `KEY` added.
  - `annotations/` — a note and a shot (`1 S1`) on scene 1.
  - `analysis/` — hand-written stubs: readiness report, brief (decisions
    `D-01`, `D-02`), worklist (`PROP-01`, `VIS-01`, `SOUND-01`).

## Key facts / gotchas

- Built from mocap-writer `d74f9f9`; rebuilding takes the writer's
  current code, so the files can change with the writer.
- Two gaps on purpose, for "ask the creator" cases: scene `2.A`'s BUS has
  no set, and the prop word `KEY` has no bible item.
- A change set's `to_hash` is the sha256 of the `scene-index.json` text it
  produced (mocap-writer `trelby/changeset.py:19-20`), not the script's
  hash: the latest change set matches the accepted index when the two
  agree.
- `bible/sync/last-sync.json` is the writer's snapshot of the accepted
  index; agents read `bible/scene-index.json`.
- `history/` lines carry the build's real times.

## Touchpoints

- `tests/test_fixture_film.py` checks it; `tools/make_fixture_film.sh`
  rebuilds it.
