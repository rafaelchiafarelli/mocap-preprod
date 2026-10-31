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
- `test_agents.py` — every agent names the film root it reads
  (`film.json`, the scene index, `mocap-contracts`; `script.fountain` for
  all but the Decision Facilitator) and no longer extracts `.docx`
  (`tests/test_agents.py:12-22`); every specialist keeps the change-set
  header (`:34-40`); the header example in `preprod.process.md` parses and
  names real scenes and a real change set of the fixture (`:43`).
- `fixtures/` — test data (its own `CLAUDE.md`).

## Key facts / gotchas

- Runs only in the image: `mocap_contracts` is not installed on the host.

## Touchpoints

- `docker/` (the image), `scripts/sync_agents.py` (checked),
  `tools/make_fixture_film.sh` (rebuilds `fixtures/film/`).
