## 3. Architecture decision record

- **Depends on:** workflow-model/1 and workflow-model/2
- **Contract:**
  - **In:** Accepted workflow state and user-journey/automation contracts.
  - **Requires:** Evaluation of the actual target environments, including
    Remote VS Code, custom-agent discovery, Claude Code compatibility if
    required, project-root access, multi-user handoff, persistence, security,
    and operating/maintenance cost.
  - **Delivers:** `spec/architecture-decision-record.md` comparing viable
    dashboard, persistence, integration, and automation approaches; chosen
    approach (or explicit unresolved decisions); deployment and migration
    boundaries; and contracts for dashboard and automation epics.
- **Pre-work:** Tasks 1 and 2 reviewed; verify supported platform capabilities
  from authoritative documentation before depending on them.
- **Out of scope:** Implementing the selected architecture; assuming a cloud
  service, database, hook API, or always-on machine without explicit
  evaluation.
- **Acceptance checks:**
  - At least one viable minimum approach and its limitations are documented.
  - Platform-specific capabilities and gaps are separated from
    platform-neutral workflow data.
  - The design defines ownership, persistence, backup/export, access control,
    failure reporting, and recovery.
  - The design states exactly what can run unattended and what always needs
    human confirmation.
  - Dashboard and automation task contracts can be written without relying
    on unstated architecture decisions.
- **Tests:** Architecture review against both prior contracts and a
  documented feasibility walkthrough in the intended remote environment.
