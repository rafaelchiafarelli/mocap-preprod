# tools — maintenance scripts

**Role:** rebuild test data. Not used by the tests or the agents.

**Entry points:** `tools/make_fixture_film.sh [ref]` (a mocap-writer
branch or tag; default `dev`).

**Inputs → Outputs:** mocap-writer at `ref`, cloned from GitHub →
`tests/fixtures/film/` (its `analysis/` kept).

## Files

- `make_fixture_film.sh` — shallow-clones mocap-writer over HTTPS with its
  submodules (`tools/make_fixture_film.sh:14-15`), builds the writer's
  image from the clone and runs the writer's own
  `tools/make_fixture_film.py` in it (`:17-21`), replaces the fixture but
  its `analysis/` (`:23-26`), prints the writer commit it used (`:27`).

## Key facts / gotchas

- The generator lives in mocap-writer (Rafael, 2026-10-31): it uses the
  writer's code, and this repository never imports it. Cloning makes the
  rebuild work from a lone download of this repository.
- Needs Docker and network access to GitHub; no writer checkout.

## Touchpoints

- `mocap-writer` (cloned: its image and `tools/make_fixture_film.py`),
  `tests/fixtures/film/` (written).
