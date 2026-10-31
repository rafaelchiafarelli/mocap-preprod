# agents — as built

The nine agent definitions in `.claude/agents/`, as they are. Each file is
frontmatter (`name`, `description`, `tools`) plus a body that starts with
`**Display name:**` and `**Invoke with:**` lines (read by
`scripts/sync_agents.py:40`). All take a film root and write only under
`<film-root>/analysis/`. All write in the dominant language of the film's
materials (e.g. `.claude/agents/script-readiness-analyst.md:283`,
`.claude/agents/pre-production-decision-facilitator.md:241`).

## Script Readiness Analyst — `script-readiness-analyst.md`

- **Tools:** Read, Grep, Glob, Edit, Write, Bash (the only agent with Bash,
  `.claude/agents/script-readiness-analyst.md:4`).
- **Invoke with:** film root and script file (`:8`).
- **Reads:** the script and creative materials, including `.docx` (only
  `word/document.xml` when no converter exists) and PDF, as data
  (`:43-62`).
- **Triage:** splits a large film into sections, writes
  `analysis/session-plan.md` and stops (`:64-118`); section runs write
  `analysis/sections/<part>.md` (`:106`, `:211`); a consolidation run
  combines them.
- **Writes:** `analysis/pre-production-readiness.md` with a verdict
  (`:195`, `:230`), and after a whole-film assessment
  `analysis/next-session-handoff.md` naming the Decision Facilitator
  (`:120-156`).
- **Limits:** no interview (`:110`, `:117`); at most 10 questions in the
  report (`:265`).

## Pre-Production Decision Facilitator — `pre-production-decision-facilitator.md`

- **Tools:** Read, Grep, Glob, Edit, Write (`:4`).
- **Reads:** the readiness report, session plan and sections, the
  existing brief and worklist (`:33-50`).
- **Interview:** one question at a time, at most five per pass
  (`:64`); a task-scoped mode for one worklist task, at most three
  (`:84-90`).
- **Writes:** `analysis/creative-brief.md` (decision register with states
  `creator-approved`, `tentative`, `deferred`, `unresolved`; status
  `creator-reviewed for next stage` only on the creator's word, `:133`,
  `:143`) and `analysis/production-worklist.md` (stable ids, exactly one
  assigned agent by display name, statuses, `:147-224`).
- **Limits:** no design work, no script changes (`:231-239`).

## The seven specialists

Same shape in every file: **Entry and scope** (a film root and a worklist
task id; reads the task, the brief, the readiness report and the relevant
script passages; stops on a routing mismatch with the task's `Assigned
agent`), **Work**, **Bounded creator decisions** (at most three questions,
one recommendation and at most one alternative), **Production-facing
specification** (a structured register with stable ids and a state per
entry), **Deliverable and handoff** (one memo, and only that task's
worklist row). Tools: Read, Grep, Glob, Edit, Write.

| Agent | File | Memo `analysis/work/<task-id>-…` | Questions | States used |
|---|---|---|---|---|
| Story & Editorial Analyst | `story-editorial-analyst.md` | `story-editorial.md` (`:83`) | `:55` | `script-stated`, `creator-approved`, `proposal`, `TBD` |
| Visual Development Analyst | `visual-development-analyst.md` | `visual-development.md` (`:70`) | none (bug, below) | `established`, `creator-approved`, `proposal`, `TBD` (`:59`) |
| Character Design Planner | `character-design-planner.md` | `character-design.md` (`:77`) | `:48` | `established`, `creator-approved`, `proposal`, `TBD` (`:66`) |
| Performance & Editorial Planner | `performance-editorial-planner.md` | `performance-editorial.md` (`:83`) | `:54` | `script-stated`, `creator-approved`, `proposal`, `TBD` (`:73`) |
| Props & Continuity Planner | `props-continuity-planner.md` | `props-continuity.md` (`:79`) | `:51` | `script-stated`, `creator-approved`, `proposal`, `TBD` (`:69`) |
| Sound Design Planner | `sound-design-planner.md` | `sound-design.md` (`:76`) | `:49` | `script-stated`, `creator-approved`, `proposal`, `TBD` |
| Cinematography Planner | `cinematography-planner.md` | `cinematography.md` (`:78`) | `:49` | `creator-approved`, `proposal`, `TBD` (`:68`) |

The edit limit ("the only files this agent may edit") is at
`story-editorial-analyst.md:92`, `visual-development-analyst.md:79`,
`character-design-planner.md:86`, `performance-editorial-planner.md:92`,
`props-continuity-planner.md:88`, `sound-design-planner.md:84`,
`cinematography-planner.md:87`. It is an instruction, not a permission:
Edit and Write reach the whole workspace.

## Key facts / gotchas

- The Visual Development Analyst has no "Bounded creator decisions"
  section, so no question cap or option limit
  ([bug agents/1](initiatives/bugs/epics/agents/tasks/1-visual-development-no-question-cap.md)).
- The specialists' state words differ (`established` vs `script-stated`;
  Cinematography has neither) and don't match the bible's value states
  ([bug agents/2](initiatives/bugs/epics/agents/tasks/2-value-states-differ.md)).
- The Readiness Analyst writes suggested prompts
  (`script-readiness-analyst.md:87`, `:98`, `:142`) and the Facilitator a
  copyable prompt (`pre-production-decision-facilitator.md:226`); planned
  to go (`initiatives/preprod-link/epics/agents/tasks/5-no-prompts.md`).
- No agent reads `film.json`, the bible, the scene index or change sets
  yet (`initiatives/preprod-link/`).
