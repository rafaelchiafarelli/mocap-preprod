## 3. Proposals

- **Depends on:** 1, workflow-tool/2
- **Contract:** five specialists propose bible values through the tool,
  each only for the catalog groups whose department it owns:

  | Agent | Space | Departments |
  |---|---|---|
  | Visual Development Analyst | `visdev` | `art`, `lighting` |
  | Character Design Planner | `chardes` | `character-design`, `wardrobe`, `hair-makeup` |
  | Props & Continuity Planner | `props` | `props` |
  | Sound Design Planner | `sound` | `sound` |
  | Story & Editorial Analyst | `story` | `story` |

  Performance, Cinematography, the readiness analyst and the facilitator
  propose nothing. No agent covers `capture` (a capability gap, recorded
  in the agents' docs). One recommendation per field and scene goes in the
  proposal; the alternative stays in the memo. `source` is the memo; a
  change-set run passes its change set. Before proposing, an agent reads
  its reviews (`my_proposals`) and does not repeat a rejected value. A
  missing item or link is a request to the creator, never a proposal.
  Agent tools lists gain the server's tools.
- **Tests:** a proposal from each agent's documented example validates
  against the contract; adapters regenerated
