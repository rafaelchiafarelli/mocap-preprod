# Mocap Pre-Production Workhorse

This folder is the reusable pre-production workhorse for an animation-focused
production house. Keep shared worker guidance and production-house
documentation here; keep each film's script, creative decisions, and
project-specific work in that film's own project root.

## First agent

`.claude/agents/script-readiness-analyst.md` analyzes a script and
related creative materials, then turns gaps, ambiguities, and dependencies
into a prioritized set of work to complete or explicitly defer before
production. It distinguishes explicit information, ambiguity, and material
not found; it does not rewrite the script or make creative decisions.

This workflow is project-agnostic: provide the film project's root and script
when invoking the agent. It writes that project's deliverable to
`<project-root>/analysis/pre-production-readiness.md`. Do not add film-specific
paths, assumptions, or findings to this reusable workhorse documentation.

For a feature or other large, naturally divided project, the agent first
creates `<project-root>/analysis/session-plan.md`, tells you which sections
should be handled in separate sessions, and stops before claiming a complete
assessment. The plan includes suggested prompts and tracks section coverage.
Run each section in its own session; a final consolidation session combines
the section findings into the whole-project readiness report. The agent
cannot launch those sessions for you. Triage and section work do not create a
whole-project next-stage handoff; that is prepared after consolidation.

## Second agent

`.claude/agents/pre-production-decision-facilitator.md` is the next
stage after a complete readiness assessment. It checks the assessment with
the creator, asks the highest-impact questions one at a time, records
approved decisions and explicit deferrals, and creates two handoff artifacts:

- `<project-root>/analysis/creative-brief.md` — the current direction, with
  creator-approved decisions distinguished from unresolved items.
- `<project-root>/analysis/production-worklist.md` — evidence-backed tasks
  grouped by workstream, with dependencies, deliverables, completion
  conditions, and status.

The readiness assessment is not a production greenlight. The interview and
worklist are the bridge from analysis to downstream work. Later specialist
sessions read the brief and worklist, select a task marked `ready for
exploration`, and report back for creator review. They may develop options;
they do not silently turn recommendations into approved creative decisions.
The decision facilitator checks the analysis and structures the handoff, but
does not design the film itself.

Run this second agent with the project root and the completed
`analysis/pre-production-readiness.md`. For large projects, finish section
analysis and whole-project consolidation first, unless intentionally
requesting a clearly scoped section-level interview.

Suggested invocation:

> Use the Pre-Production Decision Facilitator for project root
> `<project-root>` and readiness report
> `<project-root>/analysis/pre-production-readiness.md`. Review the assessment
> with me, ask the highest-impact questions one at a time, and do not begin
> design work. Save my answers and explicit deferrals in the creative brief.
> When I say to finish this pass, create/update the production worklist with
> clear dependencies and identify the first tasks ready for specialist
> sessions.

## Specialist agents

The worklist's discipline-specific tasks can be handled by these reusable
agents in `.claude/agents/`:

- `story-editorial-analyst.md` — script alignment, narrative structure,
  and memory/editorial options.
- `visual-development-analyst.md` — environment, visual language,
  mood-board interpretation, and visual-memory options.
- `character-design-planner.md` — scoped character appearance and
  wardrobe exploration.
- `performance-editorial-planner.md` — performance beats and
  performance/image timing.
- `props-continuity-planner.md` — evidence-based prop inventories and
  continuity.
- `sound-design-planner.md` — provisional dialogue, ambience, effects,
  silence, and music cue planning.
- `cinematography-planner.md` — camera intent, framing, movement, and
  coverage exploration when a deferred task is reopened.

Each work package names exactly one assigned agent in its `Assigned agent`
column—never a team, multiple agents, or merely a suggested workstream. Each
specialist is invoked for a specific project root and worklist task ID.
That assignment is a strict routing boundary: a specialist must stop and
report a mismatch rather than take another agent's task, reassign itself, or
ask the creator whether it should expand into another discipline. It may note
an adjacent concern as a handoff, but may not do that work or edit another
task. Specialists may edit only their own task memo and that task's worklist
row; the brief, readiness report, source materials, and other tasks remain
outside their editing scope.
Each specialist reads the creative brief, readiness findings, and relevant
sources; writes a scoped memo under `<project-root>/analysis/work/`; and
updates only its selected task's status and deliverable link. They develop
options and production-facing specifications, not only narrative commentary.
Depending on the task, that artifact should be a usable beat map, shot list,
prop/material register, set/layout specification, character requirements
matrix, or sound cue sheet with stable IDs, source evidence, decision state,
and downstream dependencies. Recommendations and unknowns must be explicit.
These specs are not implementation assets: current specialists do not create
final Blender scenes, models, simulations, recordings, or mocap JSON.
Implementation is a separate task after the relevant specification and
creative choices are creator-approved. If no registered execution agent or
named human role fits, record the capability gap instead of asking a planner
to implement outside its remit or inventing a technical schema.
The current roster contains planning specialists only; it does not yet
include agents that author final production files such as mocap JSON, Blender
scenes, simulations, or rendered assets.

### Decision gates and bounded work

Specialists ask at most three task-scoped creator questions, including
clarifying follow-ups, one at a time, and only when an answer changes work
before the next named milestone or prevents material rework. Record task-local
answers/deferrals in the task memo and its worklist row; route project-wide
creative direction changes to the Decision Facilitator for the brief. The
Decision Facilitator asks at most five must-decide questions per interview
pass, including follow-ups. For everything else, record a
deferred decision with a revisit trigger and practical consequence; continue
unaffected work. A detail that can be tested in editing or addressed by a
targeted reshoot is not automatically a pre-production blocker.

Keep option sets small: normally one evidence-based recommendation and at
most one materially different alternative. Do not enumerate combinations or
turn every unknown into a new worklist row. Add a task only for a distinct
deliverable with one qualified owner that blocks a named milestone. A
creator may request a broader exploration or more interview questions.

These are agent instructions, not operating-system file permissions. Because
specialists need to write their memo and worklist status, their editor tool
still has workspace-level access; use a tool hook or other external control
if hard file-level enforcement is required.

## Running the agents

The agent definitions in `.claude/agents/` are canonical. The files in
`.github/agents/` are VS Code Copilot adapters generated from them, so don't
edit an adapter. Edit the Claude file and run:

```sh
python3 scripts/sync_agents.py          # regenerate .github/agents/
python3 scripts/sync_agents.py --check  # fails if an adapter is stale
```

**Claude Code.** Most of these agents interview the creator one question at a
time, so run each one as the main session rather than as a subagent. Start
from this repository so the agent is found, and give it the film's project
root:

```sh
cd mocap-preprod
claude --agent pre-production-decision-facilitator --add-dir <project-root>
```

Then name the project root, plus the readiness report or worklist task ID, in
the first message.

**VS Code Copilot.** Open this folder as the workspace (the remote one in
Remote VS Code), start a Copilot Chat and pick the agent from the agent picker.

## Shared production-house documentation

Reusable documentation for the production workflow should be built separately
from any one film's analysis. Since animation is the main product, this
documentation can establish shared terms and handoffs across story, assets,
scenes, animation, and sound. Keep early guidance explicit about what is
established versus still to be learned from the pilot production.

The eventual location of this workhorse within or alongside Mocap Studio is
not fixed; its contents should remain usable either way.

## Workflow dashboard

The dashboard that tracks a film's workflow, work packages and agent runs is
planned and built in `mocap-dashboard` (`initiatives/workflow-dashboard/`).
