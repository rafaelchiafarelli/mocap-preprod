# tools — maintenance scripts

**Role:** rebuild test data. Not used by the tests or the agents.

**Entry points:** `tools/make_fixture_film.sh [path to mocap-writer]`.

**Inputs → Outputs:** a `mocap-writer` checkout (default
`../mocap-writer`) → `tests/fixtures/film/` (its `analysis/` kept).

## Files

- `make_fixture_film.sh` — builds mocap-writer's image, runs the Python
  script in it with the writer mounted read-only
  (`tools/make_fixture_film.sh:13-17`), replaces the fixture but its
  `analysis/` (`:19-22`), prints the writer commit it used.
- `make_fixture_film.py` — the film made through the writer's own code:
  `Film.create`, `Bible.create`/`setValues`/`link`, the front matter, two
  annotations (`tools/make_fixture_film.py:62-104`), then a sync accepted
  on the first draft and on the edited one (`:106`, `:111`). Scripts at
  `:28` and `:51`.

## Key facts / gotchas

- `make_fixture_film.py` imports mocap-writer's code, so it runs only in
  the writer's image and nothing in this repository imports it: the
  writer is used as a tool, like a creator would use it. Repositories
  still never import each other's code.
- Needs Docker and the writer checkout beside this repository.

## Touchpoints

- `mocap-writer` (its image and code), `tests/fixtures/film/` (written).
