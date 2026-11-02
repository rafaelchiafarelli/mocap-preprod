#!/usr/bin/env bash
# Run the full test suite inside the mocap-preprod image.
#   docker/test.sh [pytest args]
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
"$repo/docker/build.sh"

exec docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$repo":/app:ro -w /app mocap-preprod:dev \
    /opt/venv/bin/python -m pytest -p no:cacheprovider "$@"
