#!/usr/bin/env python3
import json
from pathlib import Path

root = Path.cwd()
required_files = [
    "index.html","pages/capture.html","pages/frames.html","pages/stack.html","pages/about.html","README.md","LICENSE","SECURITY.md","CONTRIBUTING.md","CODE_OF_CONDUCT.md",".github/CODEOWNERS",".github/pull_request_template.md",".github/ISSUE_TEMPLATE/boundary-frame.yml",".github/ISSUE_TEMPLATE/control-gap.yml",".github/workflows/verify.yml",".github/workflows/pages.yml",".nojekyll","boundarycam-manifest.json","public-control.json","boundarycam-completion.json","data/examples.json","data/surfaces.json","data/boundarycam-live-status.json","docs/BOUNDARY_MODEL.md","docs/CONTROL_SURFACE.md","docs/FRAME_STATUS.md","docs/STACK_RELATION.md","docs/PRODUCT_CHARTER.md","docs/OPERATIONAL_DOCTRINE.md","docs/SECURITY_BOUNDARY.md","docs/ACCEPTANCE.md","docs/LIVE_SURFACE_AUDIT.md","governance/GOVERNANCE.md","security/SECURITY_BOUNDARY.md","support/SUPPORT.md","schemas/boundary-frame.schema.json","schemas/capture-event.schema.json","schemas/public-control.schema.json","schemas/boundarycam-completion.schema.json","tools/validate.py"
]
for rel in required_files:
    if not (root / rel).exists():
        raise SystemExit("MISSING_FILE=" + rel)
for rel in ["boundarycam-manifest.json","public-control.json","boundarycam-completion.json","data/examples.json","data/surfaces.json","data/boundarycam-live-status.json","schemas/boundary-frame.schema.json","schemas/capture-event.schema.json","schemas/public-control.schema.json","schemas/boundarycam-completion.schema.json"]:
    json.loads((root / rel).read_text(encoding="utf-8"))
home = (root / "index.html").read_text(encoding="utf-8")
capture = (root / "pages/capture.html").read_text(encoding="utf-8")
frames = (root / "pages/frames.html").read_text(encoding="utf-8")
readme = (root / "README.md").read_text(encoding="utf-8")
for token in ["BOUNDARYCAM", "The camera for machine action", "Capture an action"]:
    if token not in home:
        raise SystemExit("HOME_MISSING=" + token)
if "What crossed the boundary" not in capture:
    raise SystemExit("CAPTURE_MISSING_BOUNDARY_QUESTION")
if "Boundary Frames" not in frames:
    raise SystemExit("FRAMES_MISSING_TITLE")
for token in ["BOUNDARYCAM", "What crossed the boundary"]:
    if token not in readme:
        raise SystemExit("README_MISSING=" + token)
manifest = json.loads((root / "boundarycam-manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.3.0":
    raise SystemExit("MANIFEST_VERSION_INVALID")
if manifest.get("state") != "BOUNDARYCAM_PRODUCT_CONTROL_STACK_COMPLETE":
    raise SystemExit("MANIFEST_STATE_INVALID")
control = json.loads((root / "public-control.json").read_text(encoding="utf-8"))
if control.get("state") != "BOUNDARYCAM_PRODUCT_CONTROL_STACK_COMPLETE":
    raise SystemExit("CONTROL_STATE_INVALID")
completion = json.loads((root / "boundarycam-completion.json").read_text(encoding="utf-8"))
if completion.get("state") != "BOUNDARYCAM_PRODUCT_CONTROL_STACK_COMPLETE":
    raise SystemExit("COMPLETION_STATE_INVALID")
for rel in ["index.html","pages/capture.html","pages/frames.html","pages/stack.html","pages/about.html"]:
    if "```" in (root / rel).read_text(encoding="utf-8"):
        raise SystemExit("MARKDOWN_FENCE_IN_HTML=" + rel)
print("BOUNDARYCAM_COMPLETE_VALIDATE_OK=true")
