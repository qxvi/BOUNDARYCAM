set -euo pipefail
export BOUNDARYCAM_DB="${BOUNDARYCAM_DB:-/tmp/boundarycam-bundle-smoke.sqlite3}"
rm -f "$BOUNDARYCAM_DB" /tmp/boundarycam-bundle.json /tmp/boundarycam-bundle-verify.json
python3 -m boundarycam_runtime.cli capture --db "$BOUNDARYCAM_DB" --actor bundle.agent.one --action "crossed boundary one" --target "external system one" --authority "declared authority one" --execution "runtime execution one" --evidence "evidence one" --replay "replay one" --recognition "recognized one" --recourse "recourse one" --closure "closed one" >/tmp/boundarycam-frame-1.json
python3 -m boundarycam_runtime.cli capture --db "$BOUNDARYCAM_DB" --actor bundle.agent.two --action "crossed boundary two" --target "external system two" --authority "declared authority two" --execution "runtime execution two" --evidence "evidence two" --replay "replay two" --recognition "recognized two" --recourse "recourse two" --closure "closed two" >/tmp/boundarycam-frame-2.json
python3 -m boundarycam_runtime.cli export-bundle --db "$BOUNDARYCAM_DB" --out /tmp/boundarycam-bundle.json >/tmp/boundarycam-bundle.stdout.json
python3 -m boundarycam_runtime.cli verify-bundle /tmp/boundarycam-bundle.json >/tmp/boundarycam-bundle-verify.json
python3 - <<'PY'
import json
from pathlib import Path
b=json.loads(Path("/tmp/boundarycam-bundle.json").read_text())
v=json.loads(Path("/tmp/boundarycam-bundle-verify.json").read_text())
assert b["object_type"]=="BOUNDARYCAM_EVIDENCE_BUNDLE"
assert b["state"]=="BOUNDARYCAM_EVIDENCE_BUNDLE_CORE_OPEN"
assert b["frame_count"]==2
assert len(b["merkle_root"])==64
assert v["valid"] is True
PY
echo "BOUNDARYCAM_BUNDLE_SMOKE_OK=true"
