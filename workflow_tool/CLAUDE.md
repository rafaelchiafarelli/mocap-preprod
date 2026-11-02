# workflow_tool — the agents' MCP server

**Role:** the agents' only way into the film's workflow database: a stdio
MCP server on one film root. So far it only reads: `film_spaces`.

**Entry points:** `docker/mcp.sh <film-root>` (what `.mcp.json` and
`.vscode/mcp.json` start), which runs `python -m workflow_tool <film-root>`
in the image.

**Inputs → Outputs:** `<film-root>/film.json` and the database its `workflow`
part names, through `mocap_contracts` → tool results on stdout. Nothing lands
in this repository, which is mounted read-only.

## Files

- `__main__.py` — opens and closes the database once before serving
  (`workflow_tool/__main__.py:16`), so tables exist and older ones are
  migrated; a film it can't serve prints why on stderr and exits 1, without
  starting. Then serves on stdio (`:20`).
- `server.py` — `FilmError` (`workflow_tool/server.py:18`), `read_film`
  (`:25`), `workflow_path` (`:37`), `open_database` (`:44`), `agent_spaces`
  (`:48`), `check_agent` (`:53`), and `make_server` (`:61`) with the tools:
  `film_spaces(agent)` (`:65`), the agents and their space codes.

## Key facts / gotchas

- Every tool takes `agent` and refuses a name with no space in `film.json`
  (`:53`). The name is what the caller says it is: this keeps an agent to its
  own space by mistake, not by force.
- The writer owns a space but isn't an agent, so it is neither accepted nor
  listed (`:48-50`).
- The database's path comes from the `workflow` part, not a fixed name
  (`:37-41`); `workflow.sqlite` is the part's default.
- `film.json` is read on every call, so a space the writer registers while
  an agent runs is seen.
- `FilmError` must stay a `ToolError` (`:18`): SDK 2.x replaces the text of
  any other exception with "Error executing tool", and the agent wouldn't
  learn why it was refused.
- `mcp` 2.x renamed `FastMCP` to `MCPServer`, imported from
  `mcp.server.mcpserver` (`:13`).

## Touchpoints

- `mocap_contracts` (`film`, `db`, `Film`), from the image.
- `docker/mcp.sh`, `.mcp.json`, `.vscode/mcp.json`, `tests/test_workflow_tool.py`.
- `mocap-writer` `workflow-link` registers the part and the agents' spaces.
