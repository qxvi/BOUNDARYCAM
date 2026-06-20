import json
from pathlib import Path

root = Path.cwd()

required = [
    "boundarycam-whole-stack-integrity.json",
    "audit/boundarycam-whole-stack-checksums.json",
    "docs/integrity/WHOLE_STACK_INTEGRITY_LOCK.md",
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/boundarycam-live-status.json",
    "data/surfaces.json",
    "boundarycam_runtime/api.py",
    "boundarycam_runtime/store.py",
    "boundarycam_runtime/bundle.py",
    "boundarycam_runtime/merkle.py",
    "tools/runtime-smoke.sh",
    "tools/bundle-smoke.sh",
    ".github/workflows/verify.yml",
    ".github/workflows/pages.yml"
]

for rel in required:
    if not (root / rel).exists():
        raise SystemExit("MISSING_FILE=" + rel)

for rel in [
    "boundarycam-whole-stack-integrity.json",
    "audit/boundarycam-whole-stack-checksums.json",
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/boundarycam-live-status.json",
    "data/surfaces.json"
]:
    json.loads((root / rel).read_text())

for rel in ["boundarycam-manifest.json", "public-control.json", "boundarycam-completion.json"]:
    obj = json.loads((root / rel).read_text())
    if obj.get("version") != "0.7.0":
        raise SystemExit("VERSION_INVALID=" + rel)
    if obj.get("state") != "BOUNDARYCAM_WHOLE_STACK_INTEGRITY_LOCKED":
        raise SystemExit("STATE_INVALID=" + rel)

integrity = json.loads((root / "boundarycam-whole-stack-integrity.json").read_text())
if not integrity.get("runtime_core"):
    raise SystemExit("RUNTIME_CORE_FALSE")
if not integrity.get("evidence_bundle_core"):
    raise SystemExit("EVIDENCE_BUNDLE_CORE_FALSE")
if not integrity.get("cold_verification"):
    raise SystemExit("COLD_VERIFICATION_FALSE")
if not integrity.get("tamper_detection"):
    raise SystemExit("TAMPER_DETECTION_FALSE")

tracked_bad = list(root.glob("**/__pycache__/*.pyc"))
if tracked_bad:
    raise SystemExit("PYC_PRESENT")

print("BOUNDARYCAM_V070_VALIDATE_OK=true")
