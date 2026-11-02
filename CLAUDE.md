# mocap-preprod — the pre-production agents of the workhorse

**Role:** holds the agent definitions that run the pre-production stage of
the workhorse on one film at a time: script readiness analysis, the
creator's decision interview, and seven specialists that each take one
worklist task. One script keeps the Copilot adapters in step with the
Claude agents; a Docker image runs the tests.

**Entry points:** `claude --agent <name> --add-dir <film-root>` from this
folder (`README.md`, "Running the agents"); `python3 scripts/sync_agents.py`
after editing an agent; `make test` for the test suite.

**Inputs → Outputs:** a film root kept by `mocap-writer` (script, scene
index, bible, annotations, creative materials) →
Markdown under `<film-root>/analysis/` (readiness report, brief, worklist,
memos). Nothing an agent writes lands in this repository.

## Files

- `README.md` — what each agent does and how to run them.
- `preprod.process.md` — the stages the agents run, stage by stage.
- `agents.as-built.md` — each agent file as it is: tools, reads, writes,
  limits, with `file:line`. It documents `.claude/agents/`, which can't
  hold a `CLAUDE.md` (see gotchas).
- `.claude/agents/*.md` — the nine canonical agent definitions
  (`agents.as-built.md`).
- `.claude/skills/mocap-workflow/` — the shared process skill, a copy kept
  in step with `mocap-studio`.
- `.github/agents/` — Copilot adapters generated from `.claude/agents/`
  (its own `CLAUDE.md`).
- `scripts/` — `sync_agents.py` (its own `CLAUDE.md`).
- `Makefile` — `make test`, the suite in the image.
- `pytest.ini` — tests under `tests/`.
- `docker/` — the test image (its own `CLAUDE.md`).
- `tests/` — the test suite and the neutral fixture film root (its own
  `CLAUDE.md`).
- `tools/` — rebuilds the fixture film with mocap-writer's generator,
  cloned from GitHub (its own `CLAUDE.md`).
- `initiatives/` — planned work and the bug backlog (`initiatives/README.md`).

## Key facts / gotchas

- `.claude/agents/` holds agent files only: `scripts/sync_agents.py:66`
  reads every `*.md` there as an agent and fails on one without
  frontmatter (`scripts/sync_agents.py:30`), and Claude Code loads agents
  from it. Its as-built lives in `agents.as-built.md` here.
- The agents read the film root `mocap-writer` keeps (`film.json`, the
  script, the scene index, the bible, annotations) and write Markdown
  under `analysis/` only; proposals and requests to the writer are planned
  (`initiatives/preprod-link/`). Formats come from the `mocap-contracts`
  checkout beside this repository (`agents.as-built.md`).
- "Not broken" for this repository: `make test` passes (it includes
  `sync_agents.py --check`), and links and referenced paths resolve.
- `mocap-contracts` is not pinned: the image takes its newest release
  (`docker/CLAUDE.md`).

## Touchpoints

- Film roots (outside every repository): read and written by the agents.
- `mocap-writer`: keeps the film root the agents will read
  (`preprod-link`).
- `mocap-dashboard`: tracks a film's workflow, reads the same `analysis/`
  files.
- `mocap-studio`: holds this repository as a submodule and the canonical
  `mocap-workflow` skill.
