import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from boundarycam_runtime.admissibility import check_public_inspection_admissibility

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    obj = json.loads(Path(args.path).read_text())
    report = check_public_inspection_admissibility(obj)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text)

    print(text, end="")

if __name__ == "__main__":
    main()
