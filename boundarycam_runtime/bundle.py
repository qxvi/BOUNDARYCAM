from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Union
from .merkle import merkle_root, sha256_text
from .store import canonical_json

BUNDLE_VERSION = "0.6.0"
BUNDLE_TYPE = "BOUNDARYCAM_EVIDENCE_BUNDLE"

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def recompute_frame_hash(frame: Dict[str, Any]) -> str:
    data = dict(frame)
    data.pop("sequence", None)
    data.pop("frame_id", None)
    data.pop("frame_hash", None)
    return sha256_text(canonical_json(data))

def compute_bundle_hash(bundle: Dict[str, Any]) -> str:
    data = dict(bundle)
    data.pop("bundle_hash", None)
    data.pop("bundle_id", None)
    return sha256_text(canonical_json(data))

def build_bundle(frames: List[Dict[str, Any]], source: str = "boundarycam-runtime") -> Dict[str, Any]:
    ordered = sorted(frames, key=lambda f: int(f.get("sequence", 0)))
    hashes = [str(f.get("frame_hash")) for f in ordered]
    bundle = {
        "object_type": BUNDLE_TYPE,
        "version": BUNDLE_VERSION,
        "state": "BOUNDARYCAM_EVIDENCE_BUNDLE_CORE_OPEN",
        "generated_at": utc_now(),
        "source": source,
        "primary_question": "What crossed the boundary?",
        "frame_count": len(ordered),
        "first_sequence": ordered[0].get("sequence") if ordered else None,
        "last_sequence": ordered[-1].get("sequence") if ordered else None,
        "head_hash": hashes[-1] if hashes else None,
        "merkle_root": merkle_root(hashes),
        "frame_hashes": hashes,
        "frames": ordered,
        "public_only": True,
    }
    digest = compute_bundle_hash(bundle)
    bundle["bundle_hash"] = digest
    bundle["bundle_id"] = "BCAM-BUNDLE-" + digest[:16].upper()
    return bundle

def verify_bundle(bundle: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    if bundle.get("object_type") != BUNDLE_TYPE:
        errors.append("bundle object_type invalid")
    frames = bundle.get("frames") if isinstance(bundle.get("frames"), list) else []
    ordered = sorted(frames, key=lambda f: int(f.get("sequence", 0)))
    previous = None
    hashes: List[str] = []
    for frame in ordered:
        if frame.get("previous_hash") != previous:
            errors.append("previous_hash mismatch")
        if frame.get("frame_hash") != recompute_frame_hash(frame):
            errors.append("frame_hash mismatch")
        hashes.append(str(frame.get("frame_hash")))
        previous = frame.get("frame_hash")
    root = merkle_root(hashes)
    if bundle.get("frame_count") != len(ordered):
        errors.append("frame_count mismatch")
    if bundle.get("head_hash") != (hashes[-1] if hashes else None):
        errors.append("head_hash mismatch")
    if bundle.get("merkle_root") != root:
        errors.append("merkle_root mismatch")
    expected = compute_bundle_hash(bundle)
    if bundle.get("bundle_hash") != expected:
        errors.append("bundle_hash mismatch")
    if bundle.get("bundle_id") != "BCAM-BUNDLE-" + expected[:16].upper():
        errors.append("bundle_id mismatch")
    return {
        "object_type": "BOUNDARYCAM_EVIDENCE_BUNDLE_VERIFICATION",
        "version": BUNDLE_VERSION,
        "valid": not errors,
        "frame_count": len(ordered),
        "head_hash": hashes[-1] if hashes else None,
        "merkle_root": root,
        "errors": errors,
    }

def write_bundle(bundle: Dict[str, Any], path: Union[str, Path]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(bundle, indent=2) + "\n")

def read_bundle(path: Union[str, Path]) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())
