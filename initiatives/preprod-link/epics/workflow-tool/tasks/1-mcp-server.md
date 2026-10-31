## 1. The MCP server

- **Depends on:** environment/2, `mocap-contracts` `v0.8.0`
- **Contract:** a stdio MCP server in Python (`workflow_tool/`), run from
  the test image with the film root mounted at the same path; started by
  Claude Code from `.mcp.json` with the film root as its argument. It
  opens `<film-root>/workflow.sqlite` with `mocap_contracts.db` and refuses
  to start when `film.json` has no `workflow` part. Every call names the
  calling agent; the server checks it owns a space in `film.json`. Read
  tools only in this task: `film_spaces` (the agents and their codes).
  `sync_agents.py` maps the server's tools for the Copilot adapters (or
  says why it can't, flagged before going on).
- **Tests:** the server starts on the fixture with a test database and
  answers `film_spaces`; refuses an unregistered agent and a film without
  the part
