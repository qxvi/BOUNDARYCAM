from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional, Union

from .models import BoundaryFrame, BoundaryFrameInput, utc_now


SCHEMA = """
CREATE TABLE IF NOT EXISTS frames (
  sequence INTEGER PRIMARY KEY AUTOINCREMENT,
  frame_id TEXT NOT NULL UNIQUE,
  generated_at TEXT NOT NULL,
  actor TEXT NOT NULL,
  action TEXT NOT NULL,
  target TEXT NOT NULL,
  authority TEXT NOT NULL,
  execution TEXT NOT NULL,
  evidence TEXT NOT NULL,
  replay TEXT NOT NULL,
  recognition TEXT NOT NULL,
  recourse TEXT NOT NULL,
  closure TEXT NOT NULL,
  metadata_json TEXT NOT NULL,
  previous_hash TEXT,
  frame_hash TEXT NOT NULL UNIQUE,
  frame_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS receipts (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  object_type TEXT NOT NULL,
  version TEXT NOT NULL,
  generated_at TEXT NOT NULL,
  frame_count INTEGER NOT NULL,
  head_hash TEXT
);
"""


def canonical_json(obj: dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class FrameStore:
    def __init__(self, path: Union[str, Path] = "runtime/boundarycam.sqlite3") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA)
            conn.commit()

    def head_hash(self) -> Optional[str]:
        with self.connect() as conn:
            row = conn.execute("SELECT frame_hash FROM frames ORDER BY sequence DESC LIMIT 1").fetchone()
            return row["frame_hash"] if row else None

    def create_frame(self, payload: BoundaryFrameInput) -> BoundaryFrame:
        generated_at = utc_now()
        previous_hash = self.head_hash()

        base = {
            "object_type": "BOUNDARYCAM_BOUNDARY_FRAME",
            "version": "0.5.0",
            "generated_at": generated_at,
            "primary_question": "What crossed the boundary?",
            "actor": payload.actor,
            "action": payload.action,
            "target": payload.target,
            "authority": payload.authority,
            "execution": payload.execution,
            "evidence": payload.evidence,
            "replay": payload.replay,
            "recognition": payload.recognition,
            "recourse": payload.recourse,
            "closure": payload.closure,
            "metadata": payload.metadata,
            "public_only": True,
            "previous_hash": previous_hash,
        }

        digest = sha256_text(canonical_json(base))
        frame_id = "BCAM-" + digest[:16].upper()
        base["frame_id"] = frame_id
        base["frame_hash"] = digest

        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO frames (
                  frame_id, generated_at, actor, action, target, authority,
                  execution, evidence, replay, recognition, recourse, closure,
                  metadata_json, previous_hash, frame_hash, frame_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    frame_id,
                    generated_at,
                    payload.actor,
                    payload.action,
                    payload.target,
                    payload.authority,
                    payload.execution,
                    payload.evidence,
                    payload.replay,
                    payload.recognition,
                    payload.recourse,
                    payload.closure,
                    json.dumps(payload.metadata, sort_keys=True),
                    previous_hash,
                    digest,
                    json.dumps(base, indent=2, ensure_ascii=False),
                ),
            )
            sequence = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
            conn.commit()

        base["sequence"] = sequence
        frame = BoundaryFrame(**base)
        with self.connect() as conn:
            conn.execute(
                "UPDATE frames SET frame_json = ? WHERE sequence = ?",
                (frame.model_dump_json(indent=2), sequence),
            )
            conn.commit()
        return frame

    def list_frames(self, limit: int = 100) -> list[BoundaryFrame]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT frame_json FROM frames ORDER BY sequence DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [BoundaryFrame(**json.loads(row["frame_json"])) for row in rows]

    def get_frame(self, frame_id: str) -> Optional[BoundaryFrame]:
        with self.connect() as conn:
            row = conn.execute("SELECT frame_json FROM frames WHERE frame_id = ?", (frame_id,)).fetchone()
        if not row:
            return None
        return BoundaryFrame(**json.loads(row["frame_json"]))

    def verify_chain(self) -> dict[str, Any]:
        with self.connect() as conn:
            rows = conn.execute("SELECT sequence, frame_json, previous_hash, frame_hash FROM frames ORDER BY sequence ASC").fetchall()

        previous = None
        errors: list[str] = []
        for row in rows:
            data = json.loads(row["frame_json"])
            stored_hash = row["frame_hash"]
            if data.get("previous_hash") != previous:
                errors.append(f"sequence {row[sequence]} previous_hash mismatch")
            recompute_data = dict(data)
            recompute_data.pop("sequence", None)
            recompute_data.pop("frame_id", None)
            recompute_data.pop("frame_hash", None)
            recomputed = sha256_text(canonical_json(recompute_data))
            if recomputed != stored_hash:
                errors.append(f"sequence {row[sequence]} frame_hash mismatch")
            previous = stored_hash

        return {
            "object_type": "BOUNDARYCAM_CHAIN_VERIFICATION",
            "version": "0.5.0",
            "valid": len(errors) == 0,
            "frame_count": len(rows),
            "head_hash": previous,
            "errors": errors,
        }

    def receipt(self) -> dict[str, Any]:
        verification = self.verify_chain()
        return {
            "object_type": "BOUNDARYCAM_RUNTIME_RECEIPT",
            "version": "0.5.0",
            "generated_at": utc_now(),
            "frame_count": verification["frame_count"],
            "head_hash": verification["head_hash"],
            "chain_valid": verification["valid"],
        }

    def list_frames_ascending(self, limit: int = 10000) -> list[BoundaryFrame]:
        with self.connect() as conn:
            rows = conn.execute("SELECT frame_json FROM frames ORDER BY sequence ASC LIMIT ?", (limit,)).fetchall()
        return [BoundaryFrame(**json.loads(row["frame_json"])) for row in rows]
