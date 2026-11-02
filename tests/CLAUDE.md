# tests — the test suite

**Role:** what "not broken" means for this repository: `make test`
(`docker/test.sh`) green.

**Entry points:** `make test`, or `docker/test.sh -k <name>`.

**Inputs → Outputs:** the mounted repository and the image's
mocap-contracts → pass/fail; the header names the mocap-contracts tag.

## Files

- `conftest.py` — prints the mocap-contracts tag in the run's header
  (`tests/conftest.py:9-11`); fixtures `plain_film` (`:15`), a copy of the
  fixture film, and `film_root` (`:23`), that copy with the `workflow` part and
  one agent's space. The fixture comes from the writer, which registers those
  only with `workflow-link`; the plain copy is the film the server refuses.
- `mcp_client.py` — talks to `workflow_tool` as a client does, a real server
  process over stdio (`session`, `tests/mcp_client.py:21`), and `register`s
  more agents on a film.
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
  names real scenes and a real change set of the fixture (`:43`); no agent
  writes a prompt (`:56-59`) and both stages hand over with a `Next:` line
  (`:62-64`).
- `test_workflow_tool.py` — the MCP server: it answers `film_spaces`, makes
  the database where the part says, refuses an agent without a space, the
  writer, a film without the part, a broken `film.json` or database; the
  clients' config; the Copilot tool mapping.
- `test_workflow_proposals.py` — `propose` and `my_proposals`: a written
  proposal against the contract, ids and counters, units and scenes, each
  refusal (no item, outside the departments, an unregistered agent, the
  catalog, the rules, a rejected value), reviews listed, the bible untouched.
- `test_workflow_requests.py` — the request tools: a round trip between two
  agents, the answer refused to anyone but the recipient and refused twice, a
  request to the creator not answered here, each refusal, shared counters.
- `fixtures/` — test data (its own `CLAUDE.md`).

## Key facts / gotchas

- Runs only in the image: `mocap_contracts` is not installed on the host.
- Each tool call in a test starts a real server process, which is most of
  the suite's run time.

## Touchpoints

- `docker/` (the image), `scripts/sync_agents.py` (checked),
  `tools/make_fixture_film.sh` (rebuilds `fixtures/film/`).
