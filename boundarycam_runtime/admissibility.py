from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

REQUIRED_BOUNDARY_FIELDS = [
    "actor",
    "action",
    "target",
    "authority",
    "execution",
    "evidence",
    "replay",
    "recognition",
    "recourse",
    "closure",
]

OVERCLAIM_WORDS = [
    "legal proof",
    "proved legally",
    "court proof",
    "identity proof",
    "custody proof",
    "absolute truth",
    "final truth",
]

def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _text(obj: Any) -> str:
    try:
        import json
        return json.dumps(obj, sort_keys=True).lower()
    except Exception:
        return str(obj).lower()

def check_public_inspection_admissibility(obj: Dict[str, Any]) -> Dict[str, Any]:
    findings: List[str] = []
    limits: List[str] = []

    source_type = str(obj.get("object_type", "UNKNOWN"))

    candidate = obj
    if source_type == "BOUNDARYCAM_EVIDENCE_BUNDLE":
        frames = obj.get("frames") if isinstance(obj.get("frames"), list) else []
        if not frames:
            findings.append("bundle has no frames")
            limits.append("replay_limit")
        candidate = frames[0] if frames else {}

    missing = [field for field in REQUIRED_BOUNDARY_FIELDS if not candidate.get(field)]
    for field in missing:
        findings.append("missing required boundary field: " + field)

    if missing:
        limits.append("authority_limit")
        limits.append("replay_limit")

    text = _text(obj)
    overclaims = [word for word in OVERCLAIM_WORDS if word in text]
    if overclaims:
        findings.append("overclaim vocabulary present: " + ",".join(overclaims))
        limits.append("legal_limit")
        limits.append("truth_limit")

    if not candidate.get("authority"):
        findings.append("authority not inspectable")
        limits.append("authority_limit")
    if not candidate.get("execution"):
        findings.append("execution not inspectable")
        limits.append("runtime_limit")
    if not candidate.get("replay"):
        findings.append("replay not inspectable")
        limits.append("replay_limit")
    if not candidate.get("recourse"):
        findings.append("recourse not inspectable")
        limits.append("recourse_limit")

    limits = sorted(set(limits))

    if not findings:
        decision = "admissible_for_public_inspection"
        findings.append("required public boundary inspection fields present")
    elif len(missing) >= 5:
        decision = "inadmissible_for_public_inspection"
    else:
        decision = "admissible_with_limits"

    return {
        "object_type": "BOUNDARYCAM_VERIFRAX_ADMISSIBILITY_REPORT",
        "version": "0.9.0",
        "state": "BOUNDARYCAM_VERIFRAX_ADMISSIBILITY_ROUTE_OPEN",
        "checked_at": _now(),
        "source_object_type": source_type,
        "decision": decision,
        "limits": limits,
        "findings": findings,
        "non_claim": "This report types public inspection admissibility. It does not decide legal proof or final truth.",
    }
