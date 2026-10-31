#!/usr/bin/env bash
# Run the full test suite inside the mocap-preprod image.
#   docker/test.sh [pytest args]
# The image takes mocap-contracts' newest v* release tag (not pinned, DEPENDENCIES.md).
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
image="mocap-preprod:dev"
tag="$(git ls-remote --tags --refs https://github.com/rafaelchiafarelli/mocap-contracts.git 'v*' \
    | sed 's|.*refs/tags/||' | sort -V | tail -1)"
[ -n "$tag" ] || { echo "no mocap-contracts release tag found" >&2; exit 1; }
docker build -q -t "$image" --build-arg CONTRACTS_TAG="$tag" \
    -f "$repo/docker/Dockerfile" "$repo/docker" >/dev/null

exec docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$repo":/app:ro -w /app "$image" \
    /opt/venv/bin/python -m pytest -p no:cacheprovider "$@"
