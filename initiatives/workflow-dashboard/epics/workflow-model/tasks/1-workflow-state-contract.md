## 1. Workflow state contract

- **Depends on:** —
- **Contract:**
  - **In:** Current workhorse agents and documentation; representative
    project artifacts such as readiness report, session plan, creative brief,
    and production worklist.
  - **Requires:** Read-only examination of the current workflow. Do not
    modify any film project's state or assume a specific film.
  - **Delivers:** `spec/workflow-state-contract.md` defining the minimum
    project, stage, artifact, decision, work-package, assignment, dependency,
    review, and handoff fields and their allowed states.
- **Pre-work:** Inventory the current workflow stages and project artifacts.
- **Out of scope:** Selecting a database/framework; implementing a dashboard
  or hooks; inventing project decisions.
- **Acceptance checks:**
  - Each current workflow stage has entry criteria, outputs, and a
    human-review gate where applicable.
  - Each work package has exactly one assigned agent, a stable ID, dependency
    references, deliverable, completion condition, and status.
  - Creator-approved, tentative, unresolved, and deferred decisions are
    distinct states and are never silently interchangeable.
  - Missing, stale, partial, or conflicting artifacts can be represented
    without being reported as complete.
  - A second collaborator can determine the next valid action from the
    contract without relying on tacit creator knowledge.
- **Tests:** Contract review against the current readiness, session-plan,
  creative-brief, and production-worklist formats; review by a second user.
