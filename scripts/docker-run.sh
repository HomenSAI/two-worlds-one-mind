#!/usr/bin/env bash
# Run a command inside the pinned build image. Builds the image if it does not exist.
# The container only sees this repository (mounted at /work); nothing else on the computer.
set -euo pipefail
cd "$(dirname "$0")/.."
IMAGE=two-worlds-one-mind-build:1
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  docker build -t "$IMAGE" .
fi
# Git Bash on Windows rewrites paths; switch that off and use a Windows-style path for the mount.
export MSYS_NO_PATHCONV=1
if command -v cygpath >/dev/null 2>&1; then HOSTDIR="$(pwd -W)"; else HOSTDIR="$(pwd)"; fi
COMMIT="${BUILD_COMMIT:-$(git rev-parse HEAD 2>/dev/null || echo unknown)}"
exec docker run --rm \
  -e BUILD_COMMIT="$COMMIT" -e RELEASE_STATE="${RELEASE_STATE:-released}" \
  ${SOURCE_DATE_EPOCH:+-e SOURCE_DATE_EPOCH="$SOURCE_DATE_EPOCH"} \
  -v "$HOSTDIR":/work -w /work "$IMAGE" "$@"
