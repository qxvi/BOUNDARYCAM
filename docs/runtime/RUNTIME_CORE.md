# BOUNDARYCAM Runtime Core

BOUNDARYCAM v0.5.0 adds a real runtime layer.

Runtime components:

- FastAPI server
- SQLite persistence
- hash-chained Boundary Frames
- runtime receipt
- chain verification
- CLI capture command
- Dockerfile
- docker-compose
- runtime smoke test
- pytest coverage

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m uvicorn boundarycam_runtime.api:app --host 127.0.0.1 --port 4187
````

## Capture frame

```bash
curl -X POST http://127.0.0.1:4187/frames \
  -H "content-type: application/json" \
  -d @example-frame.json
```

## Verify chain

```bash
curl http://127.0.0.1:4187/chain/verify
```

State: BOUNDARYCAM_RUNTIME_CORE_OPEN.
