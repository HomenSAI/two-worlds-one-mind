#!/usr/bin/env bash
# All checks that need no build: runs inside the Docker image (or any environment with the tools installed).
#   ./scripts/check.sh            -> runs in Docker (builds the image first if needed)
#   ./scripts/check.sh --inside   -> runs directly (used inside the container and in CI)
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "${1:-}" != "--inside" ]; then
  exec ./scripts/docker-run.sh ./scripts/check.sh --inside
fi
rc=0
run() { echo "== $*"; "$@" || rc=1; }
run python3 scripts/check_meta.py
run python3 scripts/check_links.py
run python3 scripts/check_text.py
run python3 scripts/check_svg.py
run python3 scripts/selftest.py
run python3 scripts/mermaid_render.py
run python3 examples/order-table/run_example.py
run markdownlint-cli2 "**/*.md" "#node_modules" "#dist" "#tools"
if [ "$rc" -ne 0 ]; then echo "CHECKS: FAILED"; exit 1; fi
echo "CHECKS: ALL PASSED"
