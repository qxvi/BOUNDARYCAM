#!/usr/bin/env bash
set -euo pipefail
export BOUNDARYCAM_DB="${BOUNDARYCAM_DB:-runtime/boundarycam.sqlite3}"
python3 -m uvicorn boundarycam_runtime.api:app --host 127.0.0.1 --port "${PORT:-4187}"
