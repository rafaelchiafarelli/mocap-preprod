## 2. User journeys and automation policy

- **Depends on:** workflow-model/1
- **Contract:**
  - **In:** `spec/workflow-state-contract.md` and the current agent workflow.
  - **Requires:** Review of project start, analysis, multi-session section
    work, consolidation, creator interview, worklist execution, handoff,
    pause, resume, and collaborator onboarding.
  - **Delivers:** `spec/user-journeys-and-automation-policy.md` describing
    user journeys, role/approval boundaries, reminders, long-running
    operations, interruption/recovery, and observable safety requirements.
- **Pre-work:** Task 1 accepted by the initiative owner.
- **Out of scope:** Selecting a notification provider; implementing hooks,
  daemons, job queues, or UI; allowing agents to make creative decisions
  unattended.
- **Acceptance checks:**
  - Every journey identifies its user, starting condition, action, resulting
    state, handoff, and recovery path.
  - The policy distinguishes a durable reminder/checkpoint from a continuously
    running AI session; it does not imply that editor sessions or models stay
    available indefinitely.
  - Long-running or scheduled behavior is opt-in, visible, bounded, resumable,
    and cancelable, with errors surfaced rather than hidden.
  - Creative approvals, source edits, destructive changes, and external
    notifications have explicit authorization requirements.
  - Manual operation remains possible when hooks, a model, network, or
    notification service is unavailable.
- **Tests:** Walkthrough review of normal, paused, interrupted, failed, and
  handed-off scenarios with a second user.
