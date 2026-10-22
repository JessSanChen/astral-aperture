from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .gateway import JudgeSpec
from .runner import replay, run_collect, run_live, run_smoke


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="astral_b1")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("smoke", help="offline mock-judge smoke run")
    s.add_argument("--output", type=Path, required=True)
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--episodes", type=int, default=36)

    r = sub.add_parser("replay", help="rebuild report from frozen records and compare")
    r.add_argument("--input", type=Path, required=True)

    live = sub.add_parser("live", help="development run with real fixed judges via OpenRouter")
    live.add_argument("--output", type=Path, required=True)
    live.add_argument("--judges", type=Path, required=True, help="JSON file listing judge specs")
    live.add_argument("--cache-dir", type=Path, default=Path("artifacts/cache"))
    live.add_argument("--seed", type=int, default=0)
    live.add_argument("--episodes", type=int, default=36)
    live.add_argument("--workers", type=int, default=6)
    live.add_argument("--authorized", action="store_true",
                      help="required: confirms a human authorized this live development run")

    col = sub.add_parser("collect", help="collect the pilot inspection bank with real judges via OpenRouter")
    col.add_argument("--output", type=Path, required=True)
    col.add_argument("--judges", type=Path, required=True)
    col.add_argument("--cache-dir", type=Path, default=Path("artifacts/cache"))
    col.add_argument("--seed", type=int, default=1)
    col.add_argument("--per-family", type=int, default=36)
    col.add_argument("--workers", type=int, default=8)
    col.add_argument("--authorized", action="store_true")

    pil = sub.add_parser("pilot", help="offline analysis of a collected bank")
    pil.add_argument("--input", type=Path, required=True)
    args = p.parse_args(argv)

    if args.cmd == "pilot":
        from .pilot import run_pilot
        run_pilot(args.input)
        print((args.input / "pilot_report.md").read_text())
        return 0

    if args.cmd == "smoke":
        run_smoke(args.output, args.seed, args.episodes)
        print((args.output / "report.md").read_text())
        return 0
    if args.cmd == "replay":
        ok = replay(args.input)
        print("replay: identical" if ok else "replay: MISMATCH")
        return 0 if ok else 1
    if not args.authorized:
        print("live run refused: pass --authorized after human approval", file=sys.stderr)
        return 2
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("live run refused: OPENROUTER_API_KEY is not set", file=sys.stderr)
        return 2
    specs = [JudgeSpec(**j) for j in json.loads(args.judges.read_text())["judges"]]
    if args.cmd == "collect":
        summary = run_collect(args.output, specs, args.cache_dir, args.seed, args.per_family, args.workers)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    run_live(args.output, specs, args.cache_dir, args.seed, args.episodes, args.workers)
    print((args.output / "report.md").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
