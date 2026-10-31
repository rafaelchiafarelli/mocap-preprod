## 4. Requests between agents

- **Depends on:** 1, workflow-tool/3
- **Contract:** every specialist reads `my_requests` at the start of a run
  and answers the ones in its remit (`done` with where in its memo, or
  `declined` with why). An adjacent concern found in a task is a request
  to its owner (an agent or the creator) instead of a handoff paragraph;
  the memo lists the requests sent. The routing boundary stays: a request
  never makes an agent do another agent's task.
- **Tests:** the documented flow in `preprod.process.md`; adapters
  regenerated
