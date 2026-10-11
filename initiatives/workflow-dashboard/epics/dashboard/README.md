# dashboard

**Goal:** Give creators and collaborators an approachable place to start a
project and see its current workflow state, artifacts, pending decisions,
work packages, and next actions.

**Depends on:** workflow-model epic.

**Epic gate:** A second user can start or open a project, understand current
progress and blockers, find source/handoff files, and determine what can
safely happen next. It distinguishes narrative memos, production-facing
specifications, and implementation assets, and shows each one's approval
state. The dashboard does not imply that a task or decision is complete
without evidence in the state contract.

## Task order

1. `1-project-onboarding-and-status-view.md`
2. `2-work-package-board-and-handoffs.md` — depends on task 1
3. `3-collaborator-guide-and-recovery.md` — depends on tasks 1 and 2
