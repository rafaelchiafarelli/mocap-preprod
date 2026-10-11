# workflow-dashboard — mocap-preprod

**Goal:** Create a reusable dashboard and workflow-support tool that helps a
creator or production team start a film project, understand the pre-production
stages, see what has been completed and what is next, and resume work after
long gaps or across separate sessions.

**Problem:** The current workflow is described across custom agents and
project-specific Markdown files. A new or returning user must remember which
agent to run, which files to provide, what stage is complete, which work
packages are ready, and which choices still require creator approval. This
is easy to forget and difficult for other people to adopt consistently.

**Users:** The creator and other authorized production collaborators who need
to start, follow, resume, or hand off a film's pre-production workflow.

## Scope

- Make the workflow discoverable and usable without relying on the creator to
  remember its sequence.
- Support starting a project from a selected project root and tracking its
  workflow stage, required artifacts, work packages, dependencies, assigned
  specialist agent, status, required output type, approval state, and next
  action.
- Make the distinction between analysis memos, structured
  production-facing specifications, and implementation assets explicit and
  traceable through handoffs. A task cannot be considered implementation-ready
  merely because a memo exists.
- Make session handoffs and long pauses recoverable: show what was last
  completed, what remains, what decisions are open, and how to resume.
- Assess and, if a safe and supported design is established, implement
  automation hooks or reminders that can keep a process alive or bring it
  back to attention over a long period.
- Support multiple human users and make responsibility, review, and approval
  visible.
- Keep project-specific materials in each film project's root and the
  reusable dashboard/workflow definitions in this workhorse.

## Out of scope

- Making creative decisions, approving a brief, or granting production
  readiness automatically.
- Allowing unattended agents to make irreversible creative choices, rewrite
  the screenplay, create final assets, or represent unreviewed work as
  approved.
- Treating planning specialists as implementation agents. Specifications
  (such as shot lists, prop/material registers, lighting instructions, or
  cloth behavior criteria) are distinct from implementation assets (such as
  Blender scenes, rigs, simulations, mocap JSON, or recorded audio).
- Assuming that a model, editor, machine, or network connection will remain
  available indefinitely.
- Choosing a specific dashboard framework, database, hosting model,
  notification provider, or agent platform before the architecture task
  evaluates the requirements and trade-offs.
- Replacing the specialist agents or the project's source materials.

## Initiative gate

The initiative is complete when a representative user can:

1. Start a new film workflow from a project root using clear onboarding.
2. See the current stage, required and completed artifacts, open decisions,
   work packages, their single assigned agent, named deliverable type,
   dependencies, approval state, and next available action.
3. Pause and resume after a long interval or hand the project to another
   authorized person without losing workflow state or confusing proposals
   with creator-approved decisions.
4. Trace a production-facing specification to its evidence and approval,
   then identify a separate qualified execution task or explicitly show that
   no execution agent is available. Do not present specification completion
   as asset implementation.
5. Use any implemented automation only with visible status, durable
   checkpoints, explicit pause/cancel/recovery behavior, and clear
   human-approval gates.
6. Understand how to operate the workflow from built-in guidance without
   relying on the original creator's memory.

The gate requires documented evaluation of the intended editor/agent
environments, access boundaries, persistence, backup/recovery, and
notification behavior. If safe unattended execution is not feasible, the
dashboard must still provide a useful manual resume/reminder flow and state
the limitation plainly.

## Epic execution order

1. **workflow-model** — define the lifecycle, project/work-package state, user
   journeys, and architecture decisions before implementation.
2. **dashboard** — implement project start, status visibility, and
   collaboration/onboarding using the approved model.
3. **automation** — implement safe persistence, reminders, pause/resume, and
   supported hook integrations after the architecture and dashboard contracts
   are stable.

See `epics/README.md` for dependency and acceptance order. Each task file
defines one deliverable contract. Do not start implementation until its
contract, dependencies, pre-work, and tests or acceptance checks are clear.
