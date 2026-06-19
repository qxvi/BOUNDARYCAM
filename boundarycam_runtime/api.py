from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException

from . import __version__
from .models import BoundaryFrame, BoundaryFrameInput, Health
from .store import FrameStore
from .bundle import build_bundle, verify_bundle


def create_app() -> FastAPI:
    db_path = os.environ.get("BOUNDARYCAM_DB", "runtime/boundarycam.sqlite3")
    store = FrameStore(db_path)

    app = FastAPI(
        title="BOUNDARYCAM Runtime",
        version=__version__,
        description="Runtime API for machine-action Boundary Frames.",
    )

    @app.get("/healthz", response_model=Health)
    def healthz() -> Health:
        return Health(
            ok=True,
            service="BOUNDARYCAM Runtime",
            version=__version__,
            state="BOUNDARYCAM_RUNTIME_CORE_OPEN",
        )

    @app.post("/frames", response_model=BoundaryFrame)
    def create_frame(payload: BoundaryFrameInput) -> BoundaryFrame:
        return store.create_frame(payload)

    @app.get("/frames", response_model=list[BoundaryFrame])
    def list_frames(limit: int = 100) -> list[BoundaryFrame]:
        return store.list_frames(limit=max(1, min(limit, 500)))

    @app.get("/frames/{frame_id}", response_model=BoundaryFrame)
    def get_frame(frame_id: str) -> BoundaryFrame:
        frame = store.get_frame(frame_id)
        if not frame:
            raise HTTPException(status_code=404, detail="frame not found")
        return frame

    @app.get("/chain/verify")
    def verify_chain() -> dict:
        return store.verify_chain()

    @app.get("/receipt")
    def receipt() -> dict:
        return store.receipt()

    @app.get("/bundles/export")
    def export_bundle(limit: int = 10000) -> dict:
        frames = [frame.model_dump() for frame in store.list_frames_ascending(limit=max(1, min(limit, 10000)))]
        return build_bundle(frames, source="boundarycam-runtime-api")

    @app.post("/bundles/verify")
    def verify_evidence_bundle(bundle: dict) -> dict:
        return verify_bundle(bundle)

    return app


app = create_app()
