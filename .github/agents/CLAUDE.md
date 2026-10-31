# .github/agents — Copilot adapters

**Role:** the VS Code Copilot versions of the agents, one
`<name>.agent.md` per file in `.claude/agents/`.

**Entry points:** none; Copilot reads them from the agent picker.

**Inputs → Outputs:** `.claude/agents/<name>.md` →
`scripts/sync_agents.py` → `<name>.agent.md`.

## Files

- `*.agent.md` — generated, never edited by hand: each starts with a
  "Generated from" comment (`scripts/sync_agents.py:54`).

## Key facts / gotchas

- Frontmatter is rewritten for Copilot: `name` is the display name,
  `argument-hint` the "Invoke with" line, tools mapped to `read`,
  `search`, `edit`, `execute` (`scripts/sync_agents.py:19-20`, `:47-55`).
- This `CLAUDE.md` is safe here: the sync only looks at `*.agent.md`
  (`scripts/sync_agents.py:74`).

## Touchpoints

- `scripts/sync_agents.py` writes and checks these files.
