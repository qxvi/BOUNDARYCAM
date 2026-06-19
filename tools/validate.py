#!/usr/bin/env python3
import json
from pathlib import Path

root = Path.cwd()

required_files = [
    "index.html",
    "pages/capture.html",
    "pages/frames.html",
    "pages/stack.html",
    "pages/about.html",
    "app.js",
    "styles.css",
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/surfaces.json",
    "data/boundarycam-live-status.json",
    "schemas/boundary-frame.schema.json",
    "schemas/capture-event.schema.json",
    "schemas/public-control.schema.json",
    "schemas/boundarycam-completion.schema.json",
    "docs/INTERACTIVE_CONSOLE.md",
    "docs/ACCEPTANCE.md",
    "tools/live-smoke.sh",
    ".github/workflows/verify.yml",
    ".github/workflows/pages.yml"
]

for rel in required_files:
    if not (root / rel).exists():
        raise SystemExit("MISSING_FILE=" + rel)

json_files = [
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/surfaces.json",
    "data/boundarycam-live-status.json",
    "schemas/boundary-frame.schema.json",
    "schemas/capture-event.schema.json",
    "schemas/public-control.schema.json",
    "schemas/boundarycam-completion.schema.json"
]

for rel in json_files:
    json.loads((root / rel).read_text(encoding="utf-8"))

checks = {
    "index.html": ["BOUNDARYCAM", "The camera for machine action", "Capture an action", "What crossed the boundary"],
    "pages/capture.html": ["Interactive Boundary Console", "Build Boundary Frame", "What crossed the boundary"],
    "pages/frames.html": ["Boundary Frames"],
    "app.js": ["BOUNDARYCAM_BOUNDARY_FRAME", "What crossed the boundary?", "downloadFrame", "copyFrame"],
    "styles.css": ["console-layout", "json-output"]
}

for rel, tokens in checks.items():
    text = (root / rel).read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise SystemExit("MISSING_TOKEN=" + rel + ":" + token)

for rel in ["index.html", "pages/capture.html", "pages/frames.html", "pages/stack.html", "pages/about.html"]:
    if "```" in (root / rel).read_text(encoding="utf-8"):
        raise SystemExit("MARKDOWN_FENCE_IN_HTML=" + rel)

manifest = json.loads((root / "boundarycam-manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.4.0":
    raise SystemExit("MANIFEST_VERSION_INVALID")
if manifest.get("state") != "BOUNDARYCAM_INTERACTIVE_BOUNDARY_CONSOLE_OPEN":
    raise SystemExit("MANIFEST_STATE_INVALID")

control = json.loads((root / "public-control.json").read_text(encoding="utf-8"))
if control.get("state") != "BOUNDARYCAM_INTERACTIVE_BOUNDARY_CONSOLE_OPEN":
    raise SystemExit("CONTROL_STATE_INVALID")

completion = json.loads((root / "boundarycam-completion.json").read_text(encoding="utf-8"))
if completion.get("state") != "BOUNDARYCAM_INTERACTIVE_BOUNDARY_CONSOLE_OPEN":
    raise SystemExit("COMPLETION_STATE_INVALID")

print("BOUNDARYCAM_V040_VALIDATE_OK=true")
