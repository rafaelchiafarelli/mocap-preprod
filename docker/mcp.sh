#!/usr/bin/env bash
# Run the agents' MCP server on a film root, in the mocap-preprod image.
#   docker/mcp.sh <film-root>
# Started by the client (.mcp.json, .vscode/mcp.json). Stdout is the protocol.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
[ -n "${1:-}" ] || { echo "no film root: set MOCAP_FILM_ROOT" >&2; exit 2; }
film="$(cd "$1" && pwd)"
# offline, or no newer release: the image already built still serves
"$repo/docker/build.sh" || docker image inspect mocap-preprod:dev >/dev/null

# the film root keeps its own path inside, so paths the agents cite stay true
exec docker run -i --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$repo":/app:ro -v "$film":"$film" -w /app mocap-preprod:dev \
    /opt/venv/bin/python -m workflow_tool "$film"
