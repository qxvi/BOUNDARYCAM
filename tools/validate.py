import json
from pathlib import Path

root = Path.cwd()

required_files = [
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "Dockerfile",
    "docker-compose.yml",
    "boundarycam_runtime/__init__.py",
    "boundarycam_runtime/models.py",
    "boundarycam_runtime/store.py",
    "boundarycam_runtime/api.py",
    "boundarycam_runtime/cli.py",
    "runtime/run-api.sh",
    "tools/runtime-smoke.sh",
    "tests/test_runtime.py",
    "docs/runtime/RUNTIME_CORE.md",
    "docs/runtime/API.md",
    "docs/runtime/CLI.md",
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/surfaces.json",
    "data/boundarycam-live-status.json"
]

for rel in required_files:
    path = root / rel
    if not path.exists():
        raise SystemExit("MISSING_FILE=" + rel)

json_files = [
    "boundarycam-manifest.json",
    "public-control.json",
    "boundarycam-completion.json",
    "data/surfaces.json",
    "data/boundarycam-live-status.json"
]

for rel in json_files:
    json.loads((root / rel).read_text(encoding="utf-8"))

runtime_tokens = {
    "boundarycam_runtime/store.py": ["sha256", "previous_hash", "frame_hash", "verify_chain"],
    "boundarycam_runtime/api.py": ["/frames", "/chain/verify", "/receipt", "BOUNDARYCAM_RUNTIME_CORE_OPEN"],
    "boundarycam_runtime/cli.py": ["capture", "verify", "receipt"],
    "tools/runtime-smoke.sh": ["BOUNDARYCAM_RUNTIME_SMOKE_OK"],
    "Dockerfile": ["uvicorn", "4187"]
}

for rel, tokens in runtime_tokens.items():
    text = (root / rel).read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise SystemExit("MISSING_RUNTIME_TOKEN=" + rel + ":" + token)

manifest = json.loads((root / "boundarycam-manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.5.0":
    raise SystemExit("MANIFEST_VERSION_INVALID")
if manifest.get("state") != "BOUNDARYCAM_RUNTIME_CORE_OPEN":
    raise SystemExit("MANIFEST_STATE_INVALID")

control = json.loads((root / "public-control.json").read_text(encoding="utf-8"))
if control.get("state") != "BOUNDARYCAM_RUNTIME_CORE_OPEN":
    raise SystemExit("CONTROL_STATE_INVALID")

completion = json.loads((root / "boundarycam-completion.json").read_text(encoding="utf-8"))
if completion.get("state") != "BOUNDARYCAM_RUNTIME_CORE_OPEN":
    raise SystemExit("COMPLETION_STATE_INVALID")

print("BOUNDARYCAM_V050_RUNTIME_VALIDATE_OK=true")
