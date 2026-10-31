# preprod-link — epics (execution order)

1. **environment** — the test image and the neutral fixture film root (3 tasks)
2. **workflow-tool** — the MCP server the agents write through (3 tasks)
3. **agents** — read path, incremental runs, proposals, requests, no prompts (5 tasks)

`environment` first: every later task tests against its image and
fixture. `workflow-tool` needs `mocap-contracts` `v0.8.0`. In `agents`,
tasks 1, 2 and 5 need only `environment`; 3 and 4 need `workflow-tool`.
