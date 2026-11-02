# agents — as built

The nine agent definitions in `.claude/agents/`, as they are. Each file is
frontmatter (`name`, `description`, `tools`) plus a body that starts with
`**Display name:**` and `**Invoke with:**` lines (read by
`scripts/sync_agents.py:40`). All take a film root, read it as data and
write only under `<film-root>/analysis/`. All write in the dominant
language of the film's materials (e.g.
`.claude/agents/script-readiness-analyst.md:300`,
`.claude/agents/pre-production-decision-facilitator.md:257`).

## The film root they read

`mocap-writer` keeps the film root; every agent reads it the same way:
`film.json` first (the parts and their paths), the script from the
`script` part (`script.fountain`, an original in `source/` only when the
creator asks), scenes from `bible/scene-index.json`, the bible's
`item.json` files, annotations; formats from the `mocap-contracts`
checkout beside this repository; scenes cited by number (`12.A`) and
items by id (`prop-w-3`). Everything outside `analysis/` is the writer's
and is never edited. A `creator-approved` bible value counts as a
decision already made.

| Agent | Where | Also reads | Missing scene index |
|---|---|---|---|
| Script Readiness Analyst | `script-readiness-analyst.md:43-78` | all bible items, `settings/front-matter.json` (stated intent), annotations, other creative materials | works from the script, recommends a sync |
| Decision Facilitator | `pre-production-decision-facilitator.md:51-62` | all bible items (cited by id in the decision register), front matter | — (cites the index's numbers) |
| Each specialist | its `## Film root` section (table below) | the bible maps and annotation kinds of its discipline | stops: the creator accepts a sync first |

## Script Readiness Analyst — `script-readiness-analyst.md`

- **Tools:** Read, Grep, Glob, Edit, Write, Bash (the only agent with Bash,
  `.claude/agents/script-readiness-analyst.md:4`).
- **Invoke with:** the film root (`:8`).
- **Reads:** the film root as above, every file treated as data
  (`:43-78`).
- **Triage:** splits a large film into sections, writes
  `analysis/session-plan.md` and stops (`:79-134`); section runs write
  `analysis/sections/<part>.md` (`:122`, `:228`); a consolidation run
  combines them.
- **Writes:** `analysis/pre-production-readiness.md` with a verdict
  (`:212`, `:247`), and after a whole-film assessment
  `analysis/next-session-handoff.md` naming the Decision Facilitator
  (`:136-173`). Both the plan and the handoff end with plain `Next:` lines
  (agent, section or stage, files to read), never prompts (`:102`, `:158`).
- **Limits:** no interview (`:126`, `:133`); at most 10 questions in the
  report (`:282`).

## Pre-Production Decision Facilitator — `pre-production-decision-facilitator.md`

- **Tools:** Read, Grep, Glob, Edit, Write (`:4`).
- **Reads:** the readiness report, session plan and sections, the
  existing brief and worklist, and the film root (`:33-62`).
- **Interview:** one question at a time, at most five per pass
  (`:76`); a task-scoped mode for one worklist task, at most three
  (`:96-102`).
- **Writes:** `analysis/creative-brief.md` (decision register with states
  `creator-approved`, `tentative`, `deferred`, `unresolved`; status
  `creator-reviewed for next stage` only on the creator's word, `:145`,
  `:155`) and `analysis/production-worklist.md` (stable ids, exactly one
  assigned agent by display name, statuses, `:159-245`); ends with one
  `Next:` line per ready package, never a prompt (`:238`).
- **Limits:** no design work, no script changes (`:247-255`).

## The seven specialists

Same shape in every file: **Entry and scope** (a film root and a worklist
task id; reads the task, the brief, the readiness report and the relevant
script passages; stops on a routing mismatch with the task's `Assigned
agent`), **Film root**, **Change-set runs**, **Work**, **Bounded creator decisions** (at most
three questions, one recommendation and at most one alternative),
**Production-facing specification** (a structured register with stable
ids and a state per entry), **Deliverable and handoff** (one memo, and
only that task's worklist row). Tools: Read, Grep, Glob, Edit, Write.

| Agent | File | Film root | Change-set runs | Bible maps read | Memo `analysis/work/<task-id>-…` | Questions | States used |
|---|---|---|---|---|---|---|---|
| Story & Editorial Analyst | `story-editorial-analyst.md` | `:37` | `:59` | characters, sets | `story-editorial.md` (`:132`) | `:104` | `established`, `creator-approved`, `proposal`, `TBD` (`:121`) |
| Visual Development Analyst | `visual-development-analyst.md` | `:38` | `:60` | sets, props (dressing) | `visual-development.md` (`:119`) | none (bug, below) | `established`, `creator-approved`, `proposal`, `TBD` (`:108`) |
| Character Design Planner | `character-design-planner.md` | `:36` | `:58` | characters, wardrobe | `character-design.md` (`:126`) | `:97` | `established`, `creator-approved`, `proposal`, `TBD` (`:115`) |
| Performance & Editorial Planner | `performance-editorial-planner.md` | `:36` | `:58` | characters | `performance-editorial.md` (`:132`) | `:103` | `script-stated`, `creator-approved`, `proposal`, `TBD` (`:122`) |
| Props & Continuity Planner | `props-continuity-planner.md` | `:35` | `:57` | props, wardrobe (handled) | `props-continuity.md` (`:128`) | `:100` | `script-stated`, `creator-approved`, `proposal`, `TBD` (`:118`) |
| Sound Design Planner | `sound-design-planner.md` | `:35` | `:57` | sets, characters (voice) | `sound-design.md` (`:125`) | `:98` | `script-stated`, `creator-approved`, `proposal`, `TBD` (`:115`) |
| Cinematography Planner | `cinematography-planner.md` | `:37` | `:59` | sets; shots `S1`, `S2` | `cinematography.md` (`:127`) | `:98` | `creator-approved`, `proposal`, `TBD` (`:117`) |

Each memo starts with the change-set header (`Covers:`, `Change set:`,
`Not revisited:`); its grammar is in `preprod.process.md`, "Change-set
runs and the memo header". A change-set run reworks only the scenes the
change set lists and the items they link, and stops without editing when
the memo covers none of them.

The edit limit ("the only files this agent may edit") is at
`story-editorial-analyst.md:141`, `visual-development-analyst.md:128`,
`character-design-planner.md:135`, `performance-editorial-planner.md:141`,
`props-continuity-planner.md:137`, `sound-design-planner.md:133`,
`cinematography-planner.md:136`. It is an instruction, not a permission:
Edit and Write reach the whole workspace.

## Key facts / gotchas

- The Visual Development Analyst has no "Bounded creator decisions"
  section, so no question cap or option limit
  ([bug agents/1](initiatives/bugs/epics/agents/tasks/1-visual-development-no-question-cap.md)).
- The specialists' state words differ (`established` vs `script-stated`;
  Cinematography has neither) and don't match the bible's value states
  that their own Film root section names
  ([bug agents/2](initiatives/bugs/epics/agents/tasks/2-value-states-differ.md)).
- No agent writes prompts for another; a stage hands over with a plain
  `Next:` line, and only when the creator says the stage is done.
- The Readiness Analyst keeps Bash, though the `.docx` extraction it was
  for is gone.
- The `mocap-contracts` path (`../mocap-contracts/`) assumes the
  `mocap-studio` layout; a lone download of this repository has no such
  checkout.
- Nobody writes to the film root outside `analysis/` yet: proposals and
  requests come with `preprod-link` workflow-tool.
