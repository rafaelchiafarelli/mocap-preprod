## 2. Work-package board and handoffs

- **Depends on:** dashboard/1 and workflow-model/1
- **Contract:**
  - **In:** A project with a parsed or explicitly entered production worklist.
  - **Requires:** Stable task IDs, one assigned agent per task, dependency
    links, statuses, deliverables, and the approval distinctions in the
    workflow-state contract.
  - **Delivers:** A task/work-package view that identifies ready, blocked,
    deferred, in-progress, and completed work, links handoff files, and gives
    a copyable invocation for the assigned agent.
- **Pre-work:** State contract and onboarding/status view accepted.
- **Out of scope:** Running the agent without user initiation; treating
  narrative claims as verified status without artifact evidence.
- **Acceptance checks:**
  - Exactly one assigned agent is shown for each work package.
  - A task is shown as ready only when its declared dependencies and review
    gates are satisfied.
  - Users can distinguish agent output awaiting creator approval from
    approved project direction.
  - The task view presents its source files, contract, deliverable, and
    resume context.
- **Tests:** Fixture-based status/dependency tests and a collaborator
  handoff walkthrough.
