## 1. Read path

- **Depends on:** environment/2
- **Contract:** every agent reads `film.json` to find the parts, takes the
  script text from `script.fountain` (an original in `source/` only when
  asked), cites scenes by number (`12`, `12.A`) and bible items by id,
  and reads the formats from the `mocap-contracts` checkout beside this
  repository (`schema/Include/*.harpia`, `catalog/bible-v1.json`). In
  addition:

  | Agent | Also reads |
  |---|---|
  | Script Readiness Analyst | scene index (its scene list), all bible items (what is already declared), front matter (stated intent), annotations |
  | Pre-Production Decision Facilitator | bible items (`creator-approved` values count as decisions made), front matter |
  | Each specialist | scene index; the bible maps it works on; annotations of its scenes (shots for the Cinematography Planner) |

  A missing scene index is reported (the creator accepts a sync in the
  writer first), never rebuilt by the agent. The `.docx` extraction
  instructions go.
- **Tests:** each agent file names its reads; adapters regenerated;
  `sync_agents.py --check`
