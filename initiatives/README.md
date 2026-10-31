# Initiatives

The full process (initiative → epic → task → contract, branch chain, per-task
loop, stop-and-ask rules) lives in the **mocap-workflow** skill
(`.claude/skills/mocap-workflow/SKILL.md`). Read it before anything else.

Rules specific to this repository:

- **Layout:** `initiatives/<initiative>/epics/<epic>/tasks/<n>-<task>.md`.
  The number is the implementation order, and the file name is the branch name.
- **Done marker:** `-done` suffix on the **file name** (`git mv` in a separate
  commit, right after the implementation commit). Never a status line.
- **Order between epics:** in `initiatives/<initiative>/epics/README.md`.
- **Test suite:** `make test` (pytest in the Docker image, `docker/`),
  plus every link and referenced path resolving.
- **No film material** in this repository: no titles, scenes, characters or
  worklist ids. Tests use the neutral fixture film root.

The workflow-dashboard initiative moved to
`mocap-dashboard/initiatives/workflow-dashboard/` on 2026-10-11.

## Index (execution order)

| Initiative | Status |
|---|---|
| **as-built** | Done 2026-10-31 — initiative 0: `CLAUDE.md` per folder, `agents.as-built.md`, `preprod.process.md` (history: `git log -- initiatives/as-built`) |
| [bugs](bugs/bugs.md) | Open — a backlog, fixed when a bug gets in the way |
| [preprod-link](preprod-link/preprod-link.md) | Planned — the agents read the writer's film root and propose through the workflow database |
