from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import BoundaryFrameInput
from .store import FrameStore


def add_capture(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("capture", help="create a Boundary Frame")
    p.add_argument("--actor", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--authority", required=True)
    p.add_argument("--execution", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--replay", required=True)
    p.add_argument("--recognition", required=True)
    p.add_argument("--recourse", required=True)
    p.add_argument("--closure", required=True)
    p.add_argument("--metadata-json", default="{}")
    p.add_argument("--db", default="runtime/boundarycam.sqlite3")


def main() -> None:
    parser = argparse.ArgumentParser(prog="boundarycam")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_capture(sub)
    list_p = sub.add_parser("list", help="list Boundary Frames")
    list_p.add_argument("--db", default="runtime/boundarycam.sqlite3")
    list_p.add_argument("--limit", type=int, default=20)
    verify_p = sub.add_parser("verify", help="verify hash chain")
    verify_p.add_argument("--db", default="runtime/boundarycam.sqlite3")
    receipt_p = sub.add_parser("receipt", help="print runtime receipt")
    receipt_p.add_argument("--db", default="runtime/boundarycam.sqlite3")

    args = parser.parse_args()
    store = FrameStore(Path(args.db))

    if args.cmd == "capture":
        metadata = json.loads(args.metadata_json)
        payload = BoundaryFrameInput(
            actor=args.actor,
            action=args.action,
            target=args.target,
            authority=args.authority,
            execution=args.execution,
            evidence=args.evidence,
            replay=args.replay,
            recognition=args.recognition,
            recourse=args.recourse,
            closure=args.closure,
            metadata=metadata,
        )
        print(store.create_frame(payload).model_dump_json(indent=2))
        return

    if args.cmd == "list":
        print(json.dumps([f.model_dump() for f in store.list_frames(args.limit)], indent=2))
        return

    if args.cmd == "verify":
        print(json.dumps(store.verify_chain(), indent=2))
        return

    if args.cmd == "receipt":
        print(json.dumps(store.receipt(), indent=2))
        return


if __name__ == "__main__":
    main()
