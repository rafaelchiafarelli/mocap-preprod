# workflow_tool — the agents' MCP server

**Role:** the agents' only way into the film's workflow database: a stdio
MCP server on one film root. Tools: `film_spaces`, `propose`, `my_proposals`,
`send_request`, `my_requests`, `answer_request`. No agent lists them yet:
that is `initiatives/preprod-link` agents/3 and 4.

**Entry points:** `docker/mcp.sh <film-root>` (what `.mcp.json` and
`.vscode/mcp.json` start), which runs `python -m workflow_tool <film-root>`
in the image.

**Inputs → Outputs:** `<film-root>/film.json`, the bible (read only) and the
database its `workflow` part names, through `mocap_contracts` → tool results
on stdout, records in the database, the space's counter in `ids/<code>.json`.
Nothing lands in this repository, which is mounted read-only, or in the bible.

## Files

- `__main__.py` — opens and closes the database once before serving
  (`workflow_tool/__main__.py:16`), so tables exist and older ones are
  migrated; a film it can't serve prints why on stderr and exits 1, without
  starting. Then serves on stdio (`:20`).
- `server.py` — `DEPARTMENTS` (`workflow_tool/server.py:25`), `FilmError`
  (`:34`), `read_film` (`:41`), `part_path` (`:53`), `open_database` (`:60`),
  `database` (`:65`), `agent_spaces` (`:74`), `check_agent` (`:79`), `has_item`
  (`:87`), `new_id` (`:102`), `save_counter` (`:112`), `proposed_value`
  (`:127`), `was_rejected` (`:156`), `proposal_row` (`:173`), `request_row` (`:185`), and
  `make_server` (`:194`) with the tools: `film_spaces(agent)` (`:198`), the
  agents and their space codes; `propose(agent, item, field, value, source,
  scene?, note?, change_set?)` (`:208`), one proposal, returns its id;
  `my_proposals(agent, open_only?)` (`:242`), the caller's proposals, each with
  its review; `send_request(agent, to, items, scenes, what, source)` (`:258`),
  returns its id; `my_requests(agent)` (`:287`), `to_me` (open, addressed to it)
  and `answers` (to the ones it sent); `answer_request(agent, id, status,
  answer)` (`:306`), by the recipient, `done` or `declined`, once.

## Key facts / gotchas

- Every tool takes `agent` and refuses a name with no space in `film.json`
  (`:79`). The name is what the caller says it is: this keeps an agent to its
  own space by mistake, not by force.
- The writer owns a space but isn't an agent, so it is neither accepted nor
  listed (`:74-76`).
- The database's path comes from the `workflow` part, not a fixed name
  (`:53-57`); `workflow.sqlite` is the part's default.
- `film.json` is read on every call, so a space the writer registers while
  an agent runs is seen.
- `FilmError` must stay a `ToolError` (`:34`): SDK 2.x replaces the text of
  any other exception with "Error executing tool", and the agent wouldn't
  learn why it was refused.
- `mcp` 2.x renamed `FastMCP` to `MCPServer`, imported from
  `mcp.server.mcpserver` (`:19`).
- `DEPARTMENTS` is the table of `initiatives/preprod-link` agents/3, keyed by
  agent name; an agent outside it proposes nothing, and nobody owns `capture`.
  Space codes come from `film.json`, never from here.
- `propose` has no `unit` argument: a number takes the catalog field's unit
  (`:141-142`), so an agent can't give a value in another one.
- A rejection stops the same item, field, scene and value from any agent, not
  only the one who proposed it (`:156-166`). Only `rejected` stops it.
- A number is taken from `ids/<code>.json`, and the counter is written after
  the record (`:102-120`); a crash between them leaves it behind, and `new_id`
  passes numbers already held. A refused proposal takes no number.
- `has_item` scans the map's `item.json` files on each `propose`: a folder is
  named by its item's name, not its id, and thousands of proposals touch
  hundreds of items at most.
- Requests are data: the tools' descriptions say so, and nothing runs on one.
  A request to the creator is answered in the writer, never here: `creator`
  has no space, so it can't call these tools. Items and scenes may be empty,
  as a missing item has no id yet and `what` says it.
- Two agents running at once race on the counter: the same limit as the
  database, one program writes at a time.

## Touchpoints

- `mocap_contracts` (`film`, `bible`, `db`, the messages), from the image.
- `docker/mcp.sh`, `.mcp.json`, `.vscode/mcp.json`, `tests/test_workflow_tool.py`,
  `tests/test_workflow_proposals.py`, `tests/test_workflow_requests.py`.
- `mocap-writer` `workflow-link` registers the part and the agents' spaces.
