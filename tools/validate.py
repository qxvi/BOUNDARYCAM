import json
import subprocess
from pathlib import Path

root = Path.cwd()
state = "BOUNDARYCAM_VERIFRAX_ADMISSIBILITY_ROUTE_OPEN"

required = [
    "registry/contracts/verifrax-boundarycam-admissibility-vocabulary.json",
    "registry/contracts/verifrax-admissibility-sample-frame.json",
    "registry/verifrax-boundarycam-admissibility-route.json",
    "schemas/verifrax-admissibility-report.schema.json",
    "boundarycam_runtime/admissibility.py",
    "tools/check_admissibility.py",
    "docs/cross-stack/VERIFRAX_TO_BOUNDARYCAM_ADMISSIBILITY_ROUTE.md",
    "audit/boundarycam-verifrax-admissibility-route-audit.md",
    "registry/contracts/invocorder-boundarycam-capture-contract.json",
    "registry/invocorder-boundarycam-route.json",
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
    "registry/contracts/verifrax-boundarycam-admissibility-vocabulary.json",
    "registry/verifrax-boundarycam-admissibility-route.json",
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/boundarycam-live-status.json",
    "data/surfaces.json"
]:
    obj = json.loads((root / rel).read_text())
    if obj.get("state") != state:
        raise SystemExit("STATE_INVALID=" + rel)

report = subprocess.check_output([
    "python3",
    "tools/check_admissibility.py",
    "registry/contracts/verifrax-admissibility-sample-frame.json"
], text=True)
obj = json.loads(report)
if obj.get("object_type") != "BOUNDARYCAM_VERIFRAX_ADMISSIBILITY_REPORT":
    raise SystemExit("ADMISSIBILITY_REPORT_INVALID")
if obj.get("decision") != "admissible_for_public_inspection":
    raise SystemExit("ADMISSIBILITY_DECISION_INVALID")

print("BOUNDARYCAM_V090_VERIFRAX_ROUTE_VALIDATE_OK=true")
