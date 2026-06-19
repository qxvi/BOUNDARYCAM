#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${1:-https://qxvi.github.io/BOUNDARYCAM}"
curl -fsSL "$BASE_URL/" -o /tmp/boundarycam-home.html
curl -fsSL "$BASE_URL/boundarycam-manifest.json" -o /tmp/boundarycam-manifest.json
curl -fsSL "$BASE_URL/public-control.json" -o /tmp/boundarycam-public-control.json
curl -fsSL "$BASE_URL/boundarycam-completion.json" -o /tmp/boundarycam-completion.json
curl -fsSL "$BASE_URL/pages/capture.html" -o /tmp/boundarycam-capture.html
curl -fsSL "$BASE_URL/pages/frames.html" -o /tmp/boundarycam-frames.html
curl -fsSL "$BASE_URL/data/surfaces.json" -o /tmp/boundarycam-surfaces.json
grep -q "BOUNDARYCAM" /tmp/boundarycam-home.html
grep -q "The camera for machine action" /tmp/boundarycam-home.html
grep -q "Capture an action" /tmp/boundarycam-home.html
grep -q "BOUNDARYCAM_PUBLIC_MANIFEST" /tmp/boundarycam-manifest.json
grep -q "BOUNDARYCAM_PUBLIC_CONTROL" /tmp/boundarycam-public-control.json
grep -q "BOUNDARYCAM_PRODUCT_CONTROL_COMPLETION" /tmp/boundarycam-completion.json
grep -q "What crossed the boundary" /tmp/boundarycam-capture.html
grep -q "Boundary Frames" /tmp/boundarycam-frames.html
grep -q "BOUNDARYCAM_SURFACE_INDEX" /tmp/boundarycam-surfaces.json
python3 -m json.tool /tmp/boundarycam-manifest.json >/dev/null
python3 -m json.tool /tmp/boundarycam-public-control.json >/dev/null
python3 -m json.tool /tmp/boundarycam-completion.json >/dev/null
python3 -m json.tool /tmp/boundarycam-surfaces.json >/dev/null
echo "BOUNDARYCAM_LIVE_SMOKE_OK=true"
