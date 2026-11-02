#!/usr/bin/env bash
# Build the mocap-preprod image with mocap-contracts' newest v* release tag
# (not pinned, DEPENDENCIES.md). Writes nothing to stdout.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tag="$(git ls-remote --tags --refs https://github.com/rafaelchiafarelli/mocap-contracts.git 'v*' \
    | sed 's|.*refs/tags/||' | sort -V | tail -1)"
[ -n "$tag" ] || { echo "no mocap-contracts release tag found" >&2; exit 1; }
docker build -q -t mocap-preprod:dev --build-arg CONTRACTS_TAG="$tag" \
    -f "$repo/docker/Dockerfile" "$repo/docker" >/dev/null
