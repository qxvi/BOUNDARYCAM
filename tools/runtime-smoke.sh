#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-4187}"
BASE_URL="http://127.0.0.1:$PORT"
export BOUNDARYCAM_DB="${BOUNDARYCAM_DB:-/tmp/boundarycam-runtime-smoke.sqlite3}"
rm -f "$BOUNDARYCAM_DB"

python3 -m uvicorn boundarycam_runtime.api:app --host 127.0.0.1 --port "$PORT" >/tmp/boundarycam-runtime.log 2>&1 &
PID="$!"
trap "kill $PID >/dev/null 2>&1 || true" EXIT

for n in $(seq 1 50); do
  if curl -fsS "$BASE_URL/healthz" >/dev/null 2>&1; then
    break
  fi
  sleep 0.1
done

curl -fsS "$BASE_URL/healthz" | jq -e ".state == \"BOUNDARYCAM_RUNTIME_CORE_OPEN\"" >/dev/null

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

jq -e ".object_type == \"BOUNDARYCAM_BOUNDARY_FRAME\"" /tmp/boundarycam-frame.json >/dev/null
jq -e ".frame_hash | length == 64" /tmp/boundarycam-frame.json >/dev/null

curl -fsS "$BASE_URL/chain/verify" | jq -e ".valid == true and .frame_count == 1" >/dev/null
curl -fsS "$BASE_URL/receipt" | jq -e ".object_type == \"BOUNDARYCAM_RUNTIME_RECEIPT\" and .chain_valid == true" >/dev/null

echo "BOUNDARYCAM_RUNTIME_SMOKE_OK=true"
