#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-https://qxvi.github.io/BOUNDARYCAM}"

curl -fsSL "$BASE_URL/" -o /tmp/boundarycam-home.html
curl -fsSL "$BASE_URL/pages/capture.html" -o /tmp/boundarycam-capture.html
curl -fsSL "$BASE_URL/app.js" -o /tmp/boundarycam-app.js
curl -fsSL "$BASE_URL/boundarycam-manifest.json" -o /tmp/boundarycam-manifest.json
curl -fsSL "$BASE_URL/public-control.json" -o /tmp/boundarycam-public-control.json
curl -fsSL "$BASE_URL/boundarycam-completion.json" -o /tmp/boundarycam-completion.json
curl -fsSL "$BASE_URL/data/surfaces.json" -o /tmp/boundarycam-surfaces.json

grep -q "BOUNDARYCAM" /tmp/boundarycam-home.html
grep -q "The camera for machine action" /tmp/boundarycam-home.html
grep -q "Capture an action" /tmp/boundarycam-home.html
grep -q "Interactive Boundary Console" /tmp/boundarycam-capture.html
grep -q "Build Boundary Frame" /tmp/boundarycam-capture.html
grep -q "BOUNDARYCAM_BOUNDARY_FRAME" /tmp/boundarycam-app.js
grep -q "BOUNDARYCAM_INTERACTIVE_BOUNDARY_CONSOLE_OPEN" /tmp/boundarycam-manifest.json
grep -q "BOUNDARYCAM_INTERACTIVE_BOUNDARY_CONSOLE_OPEN" /tmp/boundarycam-public-control.json
grep -q "BOUNDARYCAM_INTERACTIVE_BOUNDARY_CONSOLE_OPEN" /tmp/boundarycam-completion.json

python3 -m json.tool /tmp/boundarycam-manifest.json >/dev/null
python3 -m json.tool /tmp/boundarycam-public-control.json >/dev/null
python3 -m json.tool /tmp/boundarycam-completion.json >/dev/null
python3 -m json.tool /tmp/boundarycam-surfaces.json >/dev/null

echo "BOUNDARYCAM_V040_LIVE_SMOKE_OK=true"
