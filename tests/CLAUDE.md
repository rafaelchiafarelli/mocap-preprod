# tests — the test suite

**Role:** what "not broken" means for this repository: `make test`
(`docker/test.sh`) green.

**Entry points:** `make test`, or `docker/test.sh -k <name>`.

**Inputs → Outputs:** the mounted repository and the image's
mocap-contracts → pass/fail; the header names the mocap-contracts tag.

## Files

- `conftest.py` — prints the mocap-contracts tag in the run's header
  (`tests/conftest.py:4-6`).
- `test_environment.py` — mocap-contracts imports from the image
  (`tests/test_environment.py:9-13`); the Copilot adapters are current
  (`sync_agents.py --check`, `:16-22`).
- `test_fixture_film.py` — the fixture film root: every record reads with
  `mocap_contracts` (`tests/test_fixture_film.py:22`); scene numbers,
  ids and the latest change set's hash resolve (`:42`); the worklist
  assigns registered agents (`:66`).
- `fixtures/` — test data (its own `CLAUDE.md`).

## Key facts / gotchas

- Runs only in the image: `mocap_contracts` is not installed on the host.

## Touchpoints

- `docker/` (the image), `scripts/sync_agents.py` (checked),
  `tools/make_fixture_film.sh` (rebuilds `fixtures/film/`).
