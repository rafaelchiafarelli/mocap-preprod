# docker — the test and MCP-server image

**Role:** the environment the tests (and, from `preprod-link`
workflow-tool, the agents' MCP server) run in. The agents themselves run
no Python.

**Entry points:** `docker/test.sh [pytest args]` (also `make test`);
`docker/mcp.sh <film-root>`, started by the agents' clients.

**Inputs → Outputs:** `requirements.lock` + mocap-contracts' newest `v*`
tag → image `mocap-preprod:dev`; the repository mounted read-only at
`/app` → a pytest run, or the MCP server on a film root mounted at its own
path.

## Files

- `Dockerfile` — Ubuntu 24.04 by digest (`docker/Dockerfile:5`), a venv
  from the hashed lockfile only (`:11-13`), mocap-contracts cloned at the
  build argument `CONTRACTS_TAG` into `/opt/mocap-contracts` (`:15-19`),
  on `PYTHONPATH` with its `gen/python` (`:21-22`).
- `requirements.in` — direct dependencies: `pytest`, `mcp`, `protobuf`.
- `requirements.lock` — `uv pip compile --generate-hashes` of the above
  (command in its header).
- `build.sh` — reads the newest tag with `git ls-remote`
  (`docker/build.sh:7-9`), builds with it (`:10-11`); writes nothing to stdout.
- `test.sh` — builds (`docker/test.sh:7`), runs pytest as the calling user
  (`:9-11`).
- `mcp.sh` — builds, or keeps the image it has when it can't
  (`docker/mcp.sh:11`), runs `workflow_tool` with the film root mounted
  read-write at its own path and the repository read-only (`:14-16`).

## Key facts / gotchas

- `mocap-contracts` is **not pinned** (Rafael, 2026-10-31; `DEPENDENCIES.md`
  in `mocap-studio`): each build takes the newest release. Passing the tag
  as a build argument makes a new release rebuild the clone layer; a
  cached build never hides one.
- `build.sh` needs network access to GitHub (HTTPS, no SSH keys). `test.sh`
  fails without it; `mcp.sh` serves from the image already built, so a film
  session works offline once the image exists.
- Stdout of `mcp.sh` is the MCP protocol: anything else written there breaks
  the client, which is why the build's output never goes there.
- `mcp.sh` builds on every start. A build from nothing takes longer than a
  client may wait for a server to start; `make test` once beforehand.
- Regenerate the lock after editing `requirements.in` with the `uv`
  container: `docker run --rm -u "$(id -u):$(id -g)" -e UV_CACHE_DIR=/tmp/uv
  -v "$PWD":/w -w /w ghcr.io/astral-sh/uv:0.8.22-python3.12-bookworm-slim uv
  pip compile docker/requirements.in --python-version 3.12 --python-platform
  x86_64-manylinux_2_39 --generate-hashes -o docker/requirements.lock`.

## Touchpoints

- `tests/` and `workflow_tool/` run in it; `mocap-contracts` (GitHub) is
  cloned into it.
