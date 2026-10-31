#!/usr/bin/env bash
# Rebuild tests/fixtures/film/ with mocap-writer's own generator, in its image.
#   tools/make_fixture_film.sh [ref]   (a mocap-writer branch or tag; default: dev)
# The writer is cloned fresh over HTTPS, so no checkout beside this repository is
# needed. Everything but tests/fixtures/film/analysis/ (hand-written) is replaced.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
ref="${1:-dev}"
image="mocap-writer:fixture"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

git clone -q --depth 1 --branch "$ref" --recurse-submodules --shallow-submodules \
    https://github.com/rafaelchiafarelli/mocap-writer.git "$work/writer"
mkdir "$work/out"
docker build -q -t "$image" -f "$work/writer/docker/Dockerfile" "$work/writer/docker" >/dev/null
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -e PYTHONPATH=/app:/app/third_party/mocap-contracts:/app/third_party/mocap-contracts/gen/python \
    -v "$work/writer":/app:ro -v "$work/out":/out -w /app "$image" \
    /opt/venv/bin/python tools/make_fixture_film.py /out/film

dest="$repo/tests/fixtures/film"
mkdir -p "$dest"
find "$dest" -mindepth 1 -maxdepth 1 ! -name analysis -exec rm -rf {} +
cp -r "$work/out/film/." "$dest/"
echo "built from mocap-writer $(git -C "$work/writer" rev-parse --short HEAD) ($ref)"
