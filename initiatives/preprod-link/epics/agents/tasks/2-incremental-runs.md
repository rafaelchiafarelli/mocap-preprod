## 2. Incremental runs

- **Depends on:** 1
- **Contract:** a specialist given a change set (the newest
  `bible/sync/*-changes.json` unless named) reworks only the scenes it
  lists and the items those scenes link; every specialist memo starts
  with a fixed header: `Covers:` (scenes; items), `Change set:` (file, or
  `none` on a full run), `Not revisited:` (what the memo covers that the
  change set did not touch). The header is the contract code uses to find
  which memos a change set touches.
- **Tests:** the header's grammar documented in `preprod.process.md`
  with a neutral example; adapters regenerated
