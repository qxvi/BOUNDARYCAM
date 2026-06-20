import json
import subprocess
from pathlib import Path

root = Path.cwd()
state = "BOUNDARYCAM_INVOCORDER_CAPTURE_ROUTE_OPEN"

required = [
    "registry/contracts/invocorder-boundarycam-capture-contract.json",
    "registry/contracts/invocorder-sample-capture-event.json",
    "registry/invocorder-boundarycam-route.json",
    "schemas/invocorder-capture-contract.schema.json",
    "tools/invocorder_to_boundarycam.py",
    "docs/cross-stack/INVOCORDER_TO_BOUNDARYCAM_CAPTURE_ROUTE.md",
    "audit/boundarycam-invocorder-capture-route-audit.md",
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/boundarycam-live-status.json",
    "data/surfaces.json"
]

for rel in required:
    if not (root / rel).exists():
        raise SystemExit("MISSING_FILE=" + rel)

for rel in [
    "registry/contracts/invocorder-boundarycam-capture-contract.json",
    "registry/invocorder-boundarycam-route.json",
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/boundarycam-live-status.json",
    "data/surfaces.json"
]:
    obj = json.loads((root / rel).read_text())
    if obj.get("state") != state:
        raise SystemExit("STATE_INVALID=" + rel)

mapped = subprocess.check_output([
    "python3",
    "tools/invocorder_to_boundarycam.py",
    "registry/contracts/invocorder-sample-capture-event.json"
], text=True)
obj = json.loads(mapped)
if obj.get("object_type") != "BOUNDARYCAM_CAPTURE_INPUT":
    raise SystemExit("ADAPTER_OUTPUT_INVALID")
if obj.get("source") != "INVOCORDER":
    raise SystemExit("ADAPTER_SOURCE_INVALID")

print("BOUNDARYCAM_V080_INVOCORDER_ROUTE_VALIDATE_OK=true")
