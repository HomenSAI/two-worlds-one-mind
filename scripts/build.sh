#!/usr/bin/env bash
# One command: build the complete book (PDF + self-contained HTML, English and German) into dist/,
# then check the artifacts.   ./scripts/build.sh
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "${1:-}" != "--inside" ]; then
  exec ./scripts/docker-run.sh ./scripts/build.sh --inside
fi
python3 scripts/build.py
python3 scripts/check_artifacts.py
echo "Artifacts in dist/:"; ls -l dist | grep -v '^total'
