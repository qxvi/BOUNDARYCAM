#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-4187}"
BASE_URL="http://127.0.0.1:$PORT"
export BOUNDARYCAM_DB="${BOUNDARYCAM_DB:-/tmp/boundarycam-runtime-smoke.sqlite3}"
rm -f "$BOUNDARYCAM_DB"

python3 -m uvicorn boundarycam_runtime.api:app --host 127.0.0.1 --port "$PORT" >/tmp/boundarycam-runtime.log 2>&1 &
PID="$!"
trap "kill $PID >/dev/null 2>&1 || true" EXIT

for n in $(seq 1 80); do
  if curl -fsS "$BASE_URL/healthz" >/tmp/boundarycam-health.json 2>/dev/null; then
    break
  fi
  sleep 0.1
done

python3 - <<'PY'
import json
from pathlib import Path
health = json.loads(Path("/tmp/boundarycam-health.json").read_text())
assert health["state"] == "BOUNDARYCAM_RUNTIME_CORE_OPEN"
PY

curl -fsS -X POST "$BASE_URL/frames" \
  -H "content-type: application/json" \
  -d "{
    \"actor\":\"runtime.agent\",
    \"action\":\"submitted external action\",
    \"target\":\"boundary target\",
    \"authority\":\"declared authority\",
    \"execution\":\"executed through runtime API\",
    \"evidence\":\"runtime receipt\",
    \"replay\":\"stored replay pointer\",
    \"recognition\":\"recognized boundary frame\",
    \"recourse\":\"review path declared\",
    \"closure\":\"closed by runtime smoke\"
  }" >/tmp/boundarycam-frame.json

curl -fsS "$BASE_URL/chain/verify" >/tmp/boundarycam-chain.json
curl -fsS "$BASE_URL/receipt" >/tmp/boundarycam-receipt.json

python3 - <<'PY'
import json
from pathlib import Path

frame = json.loads(Path("/tmp/boundarycam-frame.json").read_text())
assert frame["object_type"] == "BOUNDARYCAM_BOUNDARY_FRAME"
assert len(frame["frame_hash"]) == 64

chain = json.loads(Path("/tmp/boundarycam-chain.json").read_text())
assert chain["valid"] is True
assert chain["frame_count"] == 1

receipt = json.loads(Path("/tmp/boundarycam-receipt.json").read_text())
assert receipt["object_type"] == "BOUNDARYCAM_RUNTIME_RECEIPT"
assert receipt["chain_valid"] is True
PY

echo "BOUNDARYCAM_RUNTIME_SMOKE_OK=true"
