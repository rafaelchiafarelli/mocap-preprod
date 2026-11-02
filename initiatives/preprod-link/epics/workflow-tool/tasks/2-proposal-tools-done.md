## 2. Proposal tools

- **Depends on:** 1
- **Contract:** `propose(agent, item, field, value, scene?, note?,
  source, change_set?)` writes one `Proposal`: id from the agent's space,
  state `proposal`, checked by the contract rules; refused when the item
  is not in the bible, the field is outside the agent's departments
  (agents/3's table, kept in the server), or an earlier proposal with the
  same item, field, scene and value was rejected. `my_proposals(agent,
  open_only?)` lists the agent's proposals with their review (outcome,
  note, edited text). Never creates items or links.
- **Tests:** propose, list, refusal of each kind, on a test database
