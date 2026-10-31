# as-built — mocap-preprod (initiative 0)

**Goal:** the as-built docs the `mocap-workflow` skill asks for, before
the next substantial work (`preprod-link`): what the agents and scripts
in this repository do today, so each later change updates them in its
own commit.

**Scope:** a `CLAUDE.md` per folder (`.claude/agents/`, `.github/agents/`,
`scripts/`), and `preprod.process.md` at the root: the workhorse stages
these agents run, stage by stage (readiness analysis, decision interview,
specialist tasks), with each agent's inputs, outputs and limits pointing
to `file:line` in its agent file.

**Out of scope:** changing any agent.

**Initiative gate:** every `file:line` resolves; every file has its
bullet; `sync_agents.py --check` passes.

Epics: `docs` (1 task).
