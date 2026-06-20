# INVOCORDER to BOUNDARYCAM Capture Route

BOUNDARYCAM_INVOCORDER_CAPTURE_ROUTE_OPEN=true

This is Route #1 from the qxvi Power Router.

INVOCORDER supplies machine-action capture facts. BOUNDARYCAM maps those facts into a public Boundary Frame input and then exposes the frame through runtime hash-chain, runtime receipt, Evidence Bundle export, cold verification, and public inspection.

This does not merge the systems. INVOCORDER remains the recorder. BOUNDARYCAM remains the public boundary camera.

Required fields:
- actor
- action
- target
- authority
- execution
- evidence
- replay
- recognition
- recourse
- closure

Adapter:

python3 tools/invocorder_to_boundarycam.py registry/contracts/invocorder-sample-capture-event.json

Contract:

registry/contracts/invocorder-boundarycam-capture-contract.json
