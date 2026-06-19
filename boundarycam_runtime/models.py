from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field


class BoundaryFrameInput(BaseModel):
    actor: str = Field(min_length=1)
    action: str = Field(min_length=1)
    target: str = Field(min_length=1)
    authority: str = Field(min_length=1)
    execution: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    replay: str = Field(min_length=1)
    recognition: str = Field(min_length=1)
    recourse: str = Field(min_length=1)
    closure: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class BoundaryFrame(BoundaryFrameInput):
    object_type: str = "BOUNDARYCAM_BOUNDARY_FRAME"
    version: str = "0.5.0"
    frame_id: str
    sequence: int
    generated_at: str
    primary_question: str = "What crossed the boundary?"
    public_only: bool = True
    previous_hash: Optional[str] = None
    frame_hash: str


class Health(BaseModel):
    ok: bool
    service: str
    version: str
    state: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
