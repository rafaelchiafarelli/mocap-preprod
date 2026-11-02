# preprod-link — mocap-preprod

**Status:** In progress (planned by Rafael, 2026-10-31). `as-built` done
2026-10-31.

**Goal:** the agents work from the film root `mocap-writer` keeps: they
read its index, scene index, bible and change sets, cite scene numbers
and record ids, rework only what a sync touched, and leave their
proposals and requests in the film's workflow database through a tool,
for the creator to decide in the writer.

**Decided (Rafael):**
- 2026-10-24 (preprod-link in `mocap-writer`): no agent writes prompts
  for other agents; whatever can be derived from the script and the bible
  is derived by code, and the agent files stay the fixed templates. The
  link is iterative: after each sync, a specialist works only on what the
  change set touched. Agents propose and the creator decides; an agent
  never writes `creator-approved`.
- 2026-10-31: no agent on the writer side, no live connection; the writer
  reads what the agents leave with plain code.
- 2026-10-31: proposals, reviews and requests live in one SQLite database
  in the film root (`workflow.sqlite`, `mocap-contracts`
  `workflow-records`), not in JSON files, because a film can hold
  thousands of them. Agents write it through an MCP server in this
  repository (no Bash, no file editing); the writer uses the same
  generated code. The worklist and the decision register stay Markdown for
  now and move with `mocap-dashboard`'s workflow model.
- 2026-10-31: one program writes at a time (one creator). Several users or
  agents writing at once would need a central service, planned only when
  that happens.
- 2026-10-31: one id space per agent. Agents never create bible items or
  scene links; they ask the creator with a request.
- 2026-10-31: agents talk to each other through requests (data: what is
  needed, about which items and scenes, why), never through prompts.
- 2026-10-31: the readiness analyst and the decision facilitator stop
  writing prompts; a stage hands over to the next only when the creator is
  happy with it, and can be sent back for rework.
- 2026-10-31: `mocap-contracts` is not pinned here: the agents read the
  formats from the `mocap-contracts` checkout beside this repository, and
  the test image installs its newest release tag at build. A format change
  that breaks the agents shows up as a failing test.
- 2026-10-31: Docker for the test suite and the MCP server.

**Scope:** the test image and a neutral fixture film root; the MCP server
and its tools (propose, my proposals and their reviews, requests); the
agents' read path, incremental runs, proposals and requests; the
readiness analyst's and facilitator's prompts removed. Each agent change
regenerates the Copilot adapters (`scripts/sync_agents.py`) in the same
commit.

**Out of scope:** the writer's review of proposals (`mocap-writer`
`workflow-link`); which version of the script a proposal answers
(`mocap-writer` `versioning`); the worklist and decision register in the
database (`mocap-dashboard`); launching agents (`mocap-dashboard`); an
agent for the `capture` department of the bible (a capability gap, noted
in agents/3).

**Needs:** `mocap-contracts` `v0.8.0` (`workflow-records`). For the gate,
`mocap-writer` `workflow-link`.

**Initiative gate:** on the fixture film root, a specialist run cites
scene numbers and record ids, leaves a proposal and a request through the
tool; the writer lists the proposal; Rafael approves one and rejects
another; the next run of the same specialist in change-set mode reworks
only the touched scenes and does not propose the rejected value again.

Epics: `epics/README.md`.
