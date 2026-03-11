#!/usr/bin/env python3
"""
Local runner for AoC solutions.

Usage:
    python run.py 2024 1                        # reads from inputs/2024/day01.txt or stdin
    python run.py 2024 1 -i path/to/input.txt   # explicit input file
    python run.py 2024 1 --viz                  # also run visualize() and print frames
    python run.py 2024 1 --viz --frames 20      # limit visualization to N frames
"""

import argparse
import importlib.util
import sys
import time
import traceback
from pathlib import Path

# ── ANSI colours (no deps) ────────────────────────────────────────────────────
USE_COLOR = sys.stdout.isatty()

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

gold    = lambda t: _c("93", t)
green   = lambda t: _c("92", t)
red     = lambda t: _c("91", t)
dim     = lambda t: _c("2",  t)
bold    = lambda t: _c("1",  t)
cyan    = lambda t: _c("96", t)


# ── Helpers ───────────────────────────────────────────────────────────────────

def find_input(year: int, day: int) -> Path | None:
    """Return the conventional input path if it exists."""
    return next(
        (p for p in [
            Path(f"inputs/{year}/day{day:02d}.txt"),
            Path(f"inputs/{year}/{day:02d}.txt"),
            Path(f"inputs/{year}/day{day}.txt"),
        ] if p.exists()),
        None,
    )


def load_module(year: int, day: int):
    path = Path(f"solutions/{year}/day{day:02d}/solution.py")
    if not path.exists():
        print(red(f"  ✗ Not found: {path}"))
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("solution", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module, path


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run an AoC solution locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("year", type=int)
    parser.add_argument("day",  type=int)
    parser.add_argument("-i", "--input",  help="Input file (auto-detected from inputs/ if omitted)")
    parser.add_argument("--viz",          action="store_true", help="Run visualize() and print frames")
    parser.add_argument("--frames",       type=int, default=50, metavar="N",
                        help="Max frames to print from visualize() (default: 50)")
    args = parser.parse_args()

    # ── Header ────────────────────────────────────────────────────────────────
    print()
    print(f"  {gold('★')} {bold(f'AoC {args.year}  —  Day {args.day}')}")
    print(f"  {dim('─' * 36)}")

    # ── Load input ────────────────────────────────────────────────────────────
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(red(f"  ✗ Input file not found: {input_path}"))
            sys.exit(1)
        puzzle_input = input_path.read_text()
        print(f"  {dim('input')}  {input_path}  {dim(f'({len(puzzle_input.splitlines())} lines)')}")
    else:
        auto = find_input(args.year, args.day)
        if auto:
            puzzle_input = auto.read_text()
            print(f"  {dim('input')}  {auto}  {dim(f'({len(puzzle_input.splitlines())} lines)')}")
        elif sys.stdin.isatty():
            print(f"  {dim('Paste your input, then press Ctrl+D:')}")
            puzzle_input = sys.stdin.read()
        else:
            puzzle_input = sys.stdin.read()

    print()

    # ── Load solution ─────────────────────────────────────────────────────────
    module, path = load_module(args.year, args.day)
    print(f"  {dim('source')} {path}")
    print()

    if not hasattr(module, "solve"):
        print(red("  ✗ solution.py has no solve() function"))
        sys.exit(1)

    # ── Run solve() ───────────────────────────────────────────────────────────
    start = time.perf_counter()
    try:
        result = module.solve(puzzle_input)
        elapsed_ms = (time.perf_counter() - start) * 1000
    except Exception:
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(red(f"  ✗ solve() raised after {elapsed_ms:.1f} ms\n"))
        traceback.print_exc()
        sys.exit(1)

    if isinstance(result, (tuple, list)):
        part1 = str(result[0]) if len(result) > 0 else ""
        part2 = str(result[1]) if len(result) > 1 else ""
    else:
        part1, part2 = str(result), ""

    print(f"  {dim('Part 1')}  {gold(part1)}")
    if part2:
        print(f"  {dim('Part 2')}  {gold(part2)}")
    print()
    print(f"  {green('✓')} {dim(f'{elapsed_ms:.1f} ms')}")

    # ── Run visualize() ───────────────────────────────────────────────────────
    if args.viz:
        print()
        print(f"  {dim('─' * 36)}")
        if not hasattr(module, "visualize"):
            print(f"  {dim('(no visualize() function in this solution)')}")
        else:
            print(f"  {cyan('Visualization')}  {dim(f'(max {args.frames} frames)')}")
            print()
            try:
                for i, frame in enumerate(module.visualize(puzzle_input)):
                    if i >= args.frames:
                        print(dim(f"  … (stopped at {args.frames} frames, use --frames N for more)"))
                        break
                    _print_frame(i, frame)
            except Exception:
                print(red("  ✗ visualize() raised:"))
                traceback.print_exc()

    print()


def _print_frame(index: int, frame: dict) -> None:
    ftype = frame.get("type", "?")
    print(f"  {dim(f'[frame {index + 1}]')} {dim(ftype)}")

    if ftype == "text":
        for line in frame.get("lines", []):
            print(f"    {line}")

    elif ftype == "grid":
        cells = frame.get("cells", [])
        for row in cells:
            print("    " + "".join(row))

    else:
        print(f"    {frame}")

    print()


if __name__ == "__main__":
    main()
