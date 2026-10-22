"""Verify the original handoff pack, not the correctness of a research experiment."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    try:
        expected = json.loads((root / "CHECKSUMS.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Cannot read checksum manifest: {exc}", file=sys.stderr)
        return 2
    errors = []
    for relative, digest in expected.items():
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append(f"Missing or invalid path: {relative}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f"Changed content: {relative}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print("Edits after unpacking are expected to change these checksums.", file=sys.stderr)
        return 1
    print(f"Verified {len(expected)} original pack files. No scientific tests were run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
