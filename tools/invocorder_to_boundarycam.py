import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = [
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

def load_input(path):
    return json.loads(Path(path).read_text())

def map_event(event):
    missing = [field for field in REQUIRED if not event.get(field)]
    if missing:
        raise SystemExit("MISSING_FIELDS=" + ",".join(missing))
    return {
        "object_type": "BOUNDARYCAM_CAPTURE_INPUT",
        "source": "INVOCORDER",
        "mapped_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "primary_question": "What crossed the boundary?",
        "actor": str(event["actor"]),
        "action": str(event["action"]),
        "target": str(event["target"]),
        "authority": str(event["authority"]),
        "execution": str(event["execution"]),
        "evidence": str(event["evidence"]),
        "replay": str(event["replay"]),
        "recognition": str(event["recognition"]),
        "recourse": str(event["recourse"]),
        "closure": str(event["closure"]),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    mapped = map_event(load_input(args.input))
    text = json.dumps(mapped, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text)
    print(text, end="")

if __name__ == "__main__":
    main()
