# scripts — repository tools

**Role:** keeps the Copilot adapters in step with the canonical Claude
agents.

**Entry points:** `python3 scripts/sync_agents.py` (write) and
`python3 scripts/sync_agents.py --check` (exit 1 when an adapter is stale
or orphaned). Stdlib only.

**Inputs → Outputs:** `.claude/agents/*.md` → `.github/agents/*.agent.md`.

## Files

- `sync_agents.py` — parses each agent's frontmatter (`parse`,
  `scripts/sync_agents.py:26`), builds the adapter (`adapter`, `:38`),
  writes or checks every one and reports orphans (`main`, `:59`).

## Key facts / gotchas

- Every `*.md` in `.claude/agents/` is taken as an agent (`:66`); a file
  without frontmatter raises (`:30`).
- The frontmatter parser is line-based `key: value` (`:32-34`), not YAML.
- A tool missing from `TOOL_MAP` raises `KeyError` (`:44`): MCP tools
  need a mapping before an agent can list them.
- The body must hold `**Display name:**` and `**Invoke with:**` lines, or
  it raises (`:42-43`).

## Touchpoints

- `.claude/agents/` (read), `.github/agents/` (written).
