#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import json

ROOT = Path.cwd()

def fail(message):
    raise SystemExit(message)

json_files = [
    "data/examples.json",
    "data/surfaces.json",
    "boundary-schema.json",
    "public-control.json",
    "boundarycam-manifest.json",
    "schemas/boundary-frame.schema.json",
    "schemas/capture-event.schema.json",
    "schemas/public-control.schema.json",
]

for rel in json_files:
    path = ROOT / rel
    if not path.exists():
        fail("MISSING_JSON=" + rel)
    json.loads(path.read_text(encoding="utf-8"))

examples = json.loads((ROOT / "data/examples.json").read_text(encoding="utf-8"))
allowed = {"BOUNDARY INCOMPLETE", "CONTROLLED", "CLOSED"}
seen_ids = set()

required = [
    "id",
    "title",
    "actor",
    "action",
    "target",
    "authority",
    "execution",
    "evidence",
    "replay",
    "recognition",
    "recourse",
    "closure",
    "status",
    "question",
]

for item in examples:
    item_id = item.get("id", "UNKNOWN")
    missing = [key for key in required if key not in item]
    if missing:
        fail(item_id + ": missing " + ",".join(missing))

    if item_id in seen_ids:
        fail("duplicate id " + item_id)

    seen_ids.add(item_id)

    status = item.get("status")
    if status not in allowed:
        fail(item_id + ": invalid status " + str(status))

class Parser(HTMLParser):
    pass

html_files = [
    "index.html",
    "404.html",
    "pages/capture.html",
    "pages/frames.html",
    "pages/stack.html",
    "pages/about.html",
]

for rel in html_files:
    path = ROOT / rel
    if not path.exists():
        fail("MISSING_HTML=" + rel)

    html = path.read_text(encoding="utf-8")

    if "```" in html:
        fail(rel + ": markdown fence pollution")

    Parser().feed(html)

index = (ROOT / "index.html").read_text(encoding="utf-8")
for token in [
    "BOUNDARYCAM",
    "The camera for machine action.",
    "Before you trust the output, capture the boundary.",
    "If it touched the world, it needs a boundary frame.",
    "Capture an action",
]:
    if token not in index:
        fail("index missing " + token)

manifest = json.loads((ROOT / "boundarycam-manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.2.0":
    fail("MANIFEST_VERSION_NOT_020")

control = json.loads((ROOT / "public-control.json").read_text(encoding="utf-8"))
if control.get("state") != "BOUNDARYCAM_PUBLIC_CONTROL_STACK_OPEN":
    fail("CONTROL_STATE_NOT_OPEN")

print("BOUNDARYCAM_VALIDATE_OK=true")
