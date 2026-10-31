## 1. As-built docs

- **Depends on:** nothing
- **Contract:** `CLAUDE.md` in `.claude/agents/`, `.github/agents/` and
  `scripts/` in the skill's format (Role, Entry points, Inputs → Outputs,
  `## Files`, `## Key facts / gotchas`, `## Touchpoints`);
  `preprod.process.md` at the root, one section per stage and per agent:
  what it reads, what it writes under `<film-root>/analysis/`, its
  question and option limits, its routing boundary. Describes the agents
  as they are, never as they should be.
- **Tests:** links and `file:line` references resolve;
  `sync_agents.py --check` passes
