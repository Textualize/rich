#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
  pytest
  exit 0
fi

IFS=',' read -r -a files <<< "$1"
pytest "${files[@]}"
