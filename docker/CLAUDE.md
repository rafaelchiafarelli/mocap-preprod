# docker — the test and MCP-server image

**Role:** the environment the tests (and, from `preprod-link`
workflow-tool, the agents' MCP server) run in. The agents themselves run
no Python.

**Entry points:** `docker/test.sh [pytest args]` (also `make test`).

**Inputs → Outputs:** `requirements.lock` + mocap-contracts' newest `v*`
tag → image `mocap-preprod:dev`; the repository mounted read-only at
`/app` → a pytest run.

## Files

- `Dockerfile` — Ubuntu 24.04 by digest (`docker/Dockerfile:5`), a venv
  from the hashed lockfile only (`:11-13`), mocap-contracts cloned at the
  build argument `CONTRACTS_TAG` into `/opt/mocap-contracts` (`:15-19`),
  on `PYTHONPATH` with its `gen/python` (`:21-22`).
- `requirements.in` — direct dependencies: `pytest`, `mcp`, `protobuf`.
- `requirements.lock` — `uv pip compile --generate-hashes` of the above
  (command in its header).
- `test.sh` — reads the newest tag with `git ls-remote` (`docker/test.sh:9-10`),
  builds with it (`:12-13`), runs pytest as the calling user (`:15-17`).

## Key facts / gotchas

- `mocap-contracts` is **not pinned** (Rafael, 2026-10-31; `DEPENDENCIES.md`
  in `mocap-studio`): each build takes the newest release. Passing the tag
  as a build argument makes a new release rebuild the clone layer; a
  cached build never hides one.
- `test.sh` needs network access to GitHub (HTTPS, no SSH keys).
- Regenerate the lock after editing `requirements.in` with the `uv`
  container: `docker run --rm -u "$(id -u):$(id -g)" -e UV_CACHE_DIR=/tmp/uv
  -v "$PWD":/w -w /w ghcr.io/astral-sh/uv:0.8.22-python3.12-bookworm-slim uv
  pip compile docker/requirements.in --python-version 3.12 --python-platform
  x86_64-manylinux_2_39 --generate-hashes -o docker/requirements.lock`.

## Touchpoints

- `tests/` runs in it; `mocap-contracts` (GitHub) is cloned into it.
