## 3. Request tools

- **Depends on:** 2
- **Contract:** `send_request(agent, to, items, scenes, what, source)`
  (`to` another registered agent or `creator`); `my_requests(agent)` (the
  open requests addressed to it, and the answers to the ones it sent);
  `answer_request(agent, id, status, answer)` (only by the recipient).
  Requests are data, never instructions to run.
- **Tests:** a round trip between two agents; answer refused to anyone
  but the recipient
