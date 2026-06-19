set -euo pipefail

export BOUNDARYCAM_DB="${BOUNDARYCAM_DB:-/tmp/boundarycam-bundle-smoke.sqlite3}"
rm -f "$BOUNDARYCAM_DB" /tmp/boundarycam-bundle.json /tmp/boundarycam-bundle-verify.json

python3 - <<'PY'
import json
from pathlib import Path

from boundarycam_runtime.bundle import build_bundle, verify_bundle, write_bundle
from boundarycam_runtime.models import BoundaryFrameInput
from boundarycam_runtime.store import FrameStore

db = Path("/tmp/boundarycam-bundle-smoke.sqlite3")
store = FrameStore(db)

def payload(n):
    return BoundaryFrameInput(
        actor=f"bundle.agent.{n}",
        action=f"crossed boundary {n}",
        target=f"external system {n}",
        authority=f"declared authority {n}",
        execution=f"runtime execution {n}",
        evidence=f"evidence {n}",
        replay=f"replay {n}",
        recognition=f"recognized {n}",
        recourse=f"recourse {n}",
        closure=f"closed {n}",
    )

store.create_frame(payload(1))
store.create_frame(payload(2))

frames = [frame.model_dump() for frame in store.list_frames_ascending()]
bundle = build_bundle(frames, source="bundle-smoke")
write_bundle(bundle, "/tmp/boundarycam-bundle.json")

result = verify_bundle(bundle)
Path("/tmp/boundarycam-bundle-verify.json").write_text(json.dumps(result, indent=2) + "\n")

assert bundle["object_type"] == "BOUNDARYCAM_EVIDENCE_BUNDLE"
assert bundle["state"] == "BOUNDARYCAM_EVIDENCE_BUNDLE_CORE_OPEN"
assert bundle["frame_count"] == 2
assert len(bundle["merkle_root"]) == 64
assert len(bundle["bundle_hash"]) == 64
assert result["valid"] is True
assert result["frame_count"] == 2
PY

echo "BOUNDARYCAM_BUNDLE_SMOKE_OK=true"
