# scripts — repository tools

**Role:** keeps the Copilot adapters in step with the canonical Claude
agents.

**Entry points:** `python3 scripts/sync_agents.py` (write) and
`python3 scripts/sync_agents.py --check` (exit 1 when an adapter is stale
or orphaned). Stdlib only.

**Inputs → Outputs:** `.claude/agents/*.md` → `.github/agents/*.agent.md`.

## Files

- `sync_agents.py` — parses each agent's frontmatter (`parse`,
  `scripts/sync_agents.py:27`), maps tools (`copilot_tool`, `:39`), builds
  the adapter (`adapter`, `:47`),
  writes or checks every one and reports orphans (`main`, `:68`).

## Key facts / gotchas

- Every `*.md` in `.claude/agents/` is taken as an agent (`:75`); a file
  without frontmatter raises (`:31`).
- The frontmatter parser is line-based `key: value` (`:33-35`), not YAML.
- `mcp__<server>__<tool>` maps to `<server>/*` (`:39-44`), the form VS Code
  documents, so in Copilot an agent gets all of a server's tools however few
  its Claude file lists; the name is the one in `.vscode/mcp.json`. Any other
  tool missing from `TOOL_MAP` raises `KeyError` (`:44`). Not yet tried in
  Copilot.
- The body must hold `**Display name:**` and `**Invoke with:**` lines, or
  it raises (`:51-52`).

## Touchpoints

- `.claude/agents/` (read), `.github/agents/` (written).
