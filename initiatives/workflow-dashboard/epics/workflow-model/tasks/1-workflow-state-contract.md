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
    review, and handoff fields and their allowed states. Artifacts must
    distinguish analysis/memo, structured production specification, and
    implementation asset, with required format/type, evidence references,
    approval state, and producer/owner where known.
- **Pre-work:** Inventory the current workflow stages and project artifacts.
- **Out of scope:** Selecting a database/framework; implementing a dashboard
  or hooks; inventing project decisions.
- **Acceptance checks:**
  - Each current workflow stage has entry criteria, outputs, and a
    human-review gate where applicable.
  - Each work package has exactly one assigned agent, a stable ID, dependency
    references, a concrete deliverable type and contract, completion
    condition, and status.
  - A memo, specification, and implementation asset are distinct artifact
    classes; completion of one never silently satisfies another.
  - Creative approval, technical/production specification approval, and
    implementation readiness are represented separately. Unapproved
    proposals cannot be consumed as final implementation requirements.
  - If no qualified execution agent or human role is assigned, implementation
    readiness is blocked or explicitly marked as a capability gap, not
    treated as ready because a planning agent produced a document.
  - Creator-approved, tentative, unresolved, and deferred decisions are
    distinct states and are never silently interchangeable.
  - Missing, stale, partial, or conflicting artifacts can be represented
    without being reported as complete.
  - A second collaborator can determine the next valid action from the
    contract without relying on tacit creator knowledge.
- **Tests:** Contract review against the current readiness, session-plan,
  creative-brief, and production-worklist formats; review by a second user.
