from boundarycam_runtime.models import BoundaryFrameInput
from boundarycam_runtime.store import FrameStore


def payload(n: int) -> BoundaryFrameInput:
    return BoundaryFrameInput(
        actor=f"agent.{n}",
        action="external action",
        target="world boundary",
        authority="declared authority",
        execution="runtime execution",
        evidence="runtime evidence",
        replay="runtime replay",
        recognition="recognized",
        recourse="review",
        closure="closed",
    )


def test_store_creates_hash_chained_frames(tmp_path):
    store = FrameStore(tmp_path / "boundarycam.sqlite3")
    first = store.create_frame(payload(1))
    second = store.create_frame(payload(2))

    assert first.object_type == "BOUNDARYCAM_BOUNDARY_FRAME"
    assert second.previous_hash == first.frame_hash
    assert len(second.frame_hash) == 64

    verification = store.verify_chain()
    assert verification["valid"] is True
    assert verification["frame_count"] == 2
    assert verification["head_hash"] == second.frame_hash


def test_receipt(tmp_path):
    store = FrameStore(tmp_path / "boundarycam.sqlite3")
    store.create_frame(payload(1))
    receipt = store.receipt()

    assert receipt["object_type"] == "BOUNDARYCAM_RUNTIME_RECEIPT"
    assert receipt["chain_valid"] is True
    assert receipt["frame_count"] == 1
