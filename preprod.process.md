# preprod — process

The pre-production stage of the workhorse as these agents run it today,
one film root at a time. Each agent runs as the main session
(`claude --agent <name> --add-dir <film-root>`), because most interview
the creator one question at a time. Agents propose; the creator decides.
Agent details and `file:line` references: `agents.as-built.md`.

Every stage reads the film root `mocap-writer` keeps, as data: `film.json`
first, the script from `script.fountain`, scenes from
`bible/scene-index.json`, the bible's items, annotations. Scenes are cited
by number and bible items by id. Only `analysis/` is written.

## Stage 1 — Readiness analysis

**Agent:** Script Readiness Analyst. **In:** film root (script, scene
index, bible, front matter, annotations, other creative materials). **Out:** `analysis/pre-production-readiness.md`.

1. **Triage.** Estimates scope. A small film is assessed in one session; a
   large one gets `analysis/session-plan.md` (sections, coverage status)
   and the run stops (`.claude/agents/script-readiness-analyst.md:79-133`).
2. **Sections** (large films). One session per section writes
   `analysis/sections/<part>.md` and marks it `reviewed` in the plan.
3. **Consolidation** (large films). Combines the sections into the
   readiness report; refuses to treat missing sections as done.
4. **Report.** Verdict, prioritized work list, watch-outs, minimum to
   block a scene, asset and sound inventory, at most 10 questions
   (`:208-296`).
5. **Handoff.** `analysis/next-session-handoff.md` names stage 2, only
   after a whole-film assessment (`:135-171`).

## Stage 2 — Decision interview

**Agent:** Pre-Production Decision Facilitator. **In:** a complete
readiness report and the film root's bible and front matter. **Out:** `analysis/creative-brief.md`,
`analysis/production-worklist.md`.

1. **Entry checks.** Refuses whole-film work on a report pending
   consolidation; checks the report's citations
   (`.claude/agents/pre-production-decision-facilitator.md:33-62`).
2. **Interview.** At most five must-decide questions per pass, one at a
   time; the rest go to a deferred-decision register with a revisit
   trigger (`:64-132`). Progress saved to the brief after each answer.
3. **Finalize.** On the creator's word: the brief's decision register and
   the worklist, each task with one assigned agent, dependencies, a
   deliverable and a status (`:134-241`).

A task-scoped mode takes one worklist task whose outcome is a creator
decision (at most three questions, `:96-102`).

## Stage 3 — Specialist tasks

**Agents:** the seven specialists. **In:** film root and one worklist
task id; the scene index, the bible maps and annotations of its discipline. **Out:** `analysis/work/<task-id>-<discipline>.md` and that
task's worklist row.

1. **Routing.** The task's `Assigned agent` must name the agent, or it
   stops.
2. **Work.** Options and a production-facing specification with stable
   ids and a state per entry; at most three questions (except the Visual
   Development Analyst, see `agents.as-built.md`).
3. **Deliverable.** The memo, the row's status and deliverable link;
   film-wide direction changes go back to stage 2.

## What the stage does not do

No final assets (models, scenes, recordings, mocap JSON); implementation
is separate work once a specification is approved (`README.md`,
"Specialist agents").
