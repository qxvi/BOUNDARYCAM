from boundarycam_runtime.bundle import build_bundle, verify_bundle
from boundarycam_runtime.models import BoundaryFrameInput
from boundarycam_runtime.store import FrameStore

def payload(n):
    return BoundaryFrameInput(actor=f"bundle.agent.{n}", action=f"external action {n}", target="world boundary", authority="declared authority", execution="runtime execution", evidence="runtime evidence", replay="runtime replay", recognition="recognized", recourse="review", closure="closed")

def test_bundle_roundtrip(tmp_path):
    store = FrameStore(tmp_path / "bundle.sqlite3")
    store.create_frame(payload(1))
    store.create_frame(payload(2))
    bundle = build_bundle([f.model_dump() for f in store.list_frames_ascending()], source="test")
    assert bundle["object_type"] == "BOUNDARYCAM_EVIDENCE_BUNDLE"
    assert bundle["frame_count"] == 2
    assert len(bundle["bundle_hash"]) == 64
    assert verify_bundle(bundle)["valid"] is True

def test_bundle_detects_tampering(tmp_path):
    store = FrameStore(tmp_path / "bundle.sqlite3")
    store.create_frame(payload(1))
    bundle = build_bundle([f.model_dump() for f in store.list_frames_ascending()], source="test")
    bundle["frames"][0]["action"] = "tampered action"
    assert verify_bundle(bundle)["valid"] is False
