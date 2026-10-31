#!/usr/bin/env bash
# Rebuild tests/fixtures/film/ with mocap-writer's own code, in its image.
#   tools/make_fixture_film.sh [path to mocap-writer]   (default: ../mocap-writer)
# Everything but tests/fixtures/film/analysis/ (hand-written) is replaced.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
writer="$(cd "${1:-$repo/../mocap-writer}" && pwd)"
image="mocap-writer:dev"
out="$(mktemp -d)"
trap 'rm -rf "$out"' EXIT

docker build -q -t "$image" -f "$writer/docker/Dockerfile" "$writer/docker" >/dev/null
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -e PYTHONPATH=/app:/app/third_party/mocap-contracts:/app/third_party/mocap-contracts/gen/python \
    -v "$writer":/app:ro -v "$repo/tools":/tools:ro -v "$out":/out -w /app "$image" \
    /opt/venv/bin/python /tools/make_fixture_film.py /out/film

dest="$repo/tests/fixtures/film"
mkdir -p "$dest"
find "$dest" -mindepth 1 -maxdepth 1 ! -name analysis -exec rm -rf {} +
cp -r "$out/film/." "$dest/"
echo "built from mocap-writer $(git -C "$writer" rev-parse --short HEAD)"
