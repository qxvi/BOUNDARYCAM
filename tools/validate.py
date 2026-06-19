import json
from pathlib import Path
root=Path.cwd()
req=["boundarycam_runtime/merkle.py","boundarycam_runtime/bundle.py","tools/bundle-smoke.sh","tests/test_bundle.py","docs/runtime/EVIDENCE_BUNDLES.md","docs/runtime/COLD_VERIFICATION.md","docs/runtime/THREAT_MODEL.md","boundarycam-manifest.json","public-control.json","boundarycam-completion.json","data/surfaces.json","data/boundarycam-live-status.json"]
for rel in req:
    if not (root/rel).exists():
        raise SystemExit("MISSING_FILE="+rel)
for rel in ["boundarycam-manifest.json","public-control.json","boundarycam-completion.json","data/surfaces.json","data/boundarycam-live-status.json"]:
    o=json.loads((root/rel).read_text())
    if o.get("version")!="0.6.0" or o.get("state")!="BOUNDARYCAM_EVIDENCE_BUNDLE_CORE_OPEN":
        raise SystemExit("INVALID_STATE="+rel)
for rel,tokens in {"boundarycam_runtime/bundle.py":["BOUNDARYCAM_EVIDENCE_BUNDLE","verify_bundle","bundle_hash","merkle_root"],"boundarycam_runtime/merkle.py":["merkle_root"],"boundarycam_runtime/api.py":["/bundles/export","/bundles/verify"],"boundarycam_runtime/cli.py":["export-bundle","verify-bundle"]}.items():
    text=(root/rel).read_text()
    for token in tokens:
        if token not in text:
            raise SystemExit("MISSING_TOKEN="+rel+":"+token)
print("BOUNDARYCAM_V060_VALIDATE_OK=true")
