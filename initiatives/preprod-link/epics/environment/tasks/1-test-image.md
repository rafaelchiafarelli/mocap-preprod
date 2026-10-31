## 1. The test image

- **Depends on:** `as-built`
- **Pre-work:** an entry in `mocap-studio/DEPENDENCIES.md` for this
  repository, with its exception: `mocap-contracts` unpinned, newest
  release tag at build (a `mocap-studio` fix, flagged to Rafael first).
- **Contract:** `Dockerfile` (Python 3.12) and a hashed lockfile for this
  repository's own dependencies (`pytest`, the MCP SDK);
  `mocap-contracts` installed at build from its newest `v*` tag, the tag
  printed by the image and by the test run; `make test` runs `pytest` in
  the image; `sync_agents.py --check` becomes a test. The agents need no
  Python: the image is for tests and the MCP server.
- **Tests:** the suite runs in the image; a stale adapter fails it
