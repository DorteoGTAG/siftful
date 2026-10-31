from __future__ import annotations

import sys
from pathlib import Path

from .interpreter import SiftfulInterpreter


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("Usage: python -m siftful <script.sft>")
        return 1

    source_path = Path(argv[0])
    if not source_path.exists():
        print(f"File not found: {source_path}")
        return 1

    source = source_path.read_text(encoding="utf-8")
    interpreter = SiftfulInterpreter()
    try:
        out = interpreter.run(source)
        for line in out:
            print(line)
        return 0
    except Exception as exc:
        print(f"SIFTFUL error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
