#!/usr/bin/env python3
"""
Daily workflow helpers for solving Advent of Code puzzles.

Usage:
    python3 aoc.py today  [YEAR DAY]            # scaffold solution, download input, create example files
    python3 aoc.py check  [YEAR DAY]            # run solve() on the examples, then on the real input
    python3 aoc.py watch  [YEAR DAY]            # re-run check every time a file of the day is saved
    python3 aoc.py submit [YEAR DAY] --part 1   # run on the real input, submit after confirmation

YEAR and DAY default to today's puzzle (puzzles unlock at midnight US Eastern time).

Examples are filled in by hand, next to the real input (inputs/ is gitignored):
    inputs/YEAR/dayDD.example.txt     example input (add dayDD.example2.txt etc. for more)
    inputs/YEAR/dayDD.answers.json    expected answers per example; "" means "not checked"

Downloading and submitting use aocd (advent-of-code-data), which reads your session
cookie from the AOC_SESSION environment variable or ~/.config/aocd/token.
"""

import argparse
import importlib.util
import json
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo

from run import bold, dim, gold, green, red

ROOT = Path(__file__).resolve().parent
EASTERN = ZoneInfo("America/New_York")
POLL_SECONDS = 0.3

Answers = tuple[str, str]


# ── Paths ─────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Puzzle:
    year: int
    day: int
    root: Path = ROOT

    @property
    def solution_dir(self) -> Path:
        return self.root / "solutions" / str(self.year) / f"day{self.day:02d}"

    @property
    def solution(self) -> Path:
        return self.solution_dir / "solution.py"

    @property
    def input_dir(self) -> Path:
        return self.root / "inputs" / str(self.year)

    @property
    def input(self) -> Path:
        return self.input_dir / f"day{self.day:02d}.txt"

    @property
    def answers(self) -> Path:
        return self.input_dir / f"day{self.day:02d}.answers.json"

    @property
    def url(self) -> str:
        return f"https://adventofcode.com/{self.year}/day/{self.day}"

    def examples(self) -> list[Path]:
        """Example files in natural order: example, example2, ..., example10."""
        found = self.input_dir.glob(f"day{self.day:02d}.example*.txt")
        return sorted(found, key=lambda p: (len(p.name), p.name))

    def rel(self, path: Path) -> str:
        return str(path.relative_to(self.root))


def example_name(path: Path) -> str:
    """'day01.example2.txt' -> 'example2' (the key used in answers.json)."""
    return path.name.split(".")[1]


def today_puzzle(now: datetime | None = None) -> tuple[int, int] | None:
    """Today's (year, day) during the event, in the puzzle's own time zone."""
    now = now or datetime.now(EASTERN)
    if now.month == 12 and now.day <= 25:
        return now.year, now.day
    return None


# ── Running a solution ────────────────────────────────────────────────────────

def load_solution(puzzle: Puzzle):
    """Import solution.py fresh, so module-level state never leaks between runs."""
    year_dir = str(puzzle.solution_dir.parent)
    if year_dir not in sys.path:
        sys.path.insert(0, year_dir)  # shared modules such as intcode.py
    spec = importlib.util.spec_from_file_location("solution", puzzle.solution)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def run_solve(puzzle: Puzzle, text: str) -> tuple[Answers, float]:
    """Run solve() on one input. Returns the answers as strings and the time in ms."""
    module = load_solution(puzzle)
    start = time.perf_counter()
    result = module.solve(text)
    elapsed_ms = (time.perf_counter() - start) * 1000
    if not isinstance(result, (tuple, list)):
        result = (result, "")
    parts = [str(value).strip() for value in result[:2]]
    parts += [""] * (2 - len(parts))
    return (parts[0], parts[1]), elapsed_ms


def load_expected(puzzle: Puzzle) -> dict[str, dict[str, str]]:
    if not puzzle.answers.exists():
        return {}
    try:
        return json.loads(puzzle.answers.read_text())
    except json.JSONDecodeError as error:
        print(red(f"  ✗ {puzzle.rel(puzzle.answers)} is not valid JSON: {error}"))
        return {}


def header(puzzle: Puzzle, action: str) -> None:
    print()
    print(f"  {gold('★')} {bold(f'AoC {puzzle.year}  Day {puzzle.day}')}  {dim(action)}")
    print(f"  {dim('─' * 36)}")


# ── check ─────────────────────────────────────────────────────────────────────

def check(puzzle: Puzzle, force_real: bool = False) -> tuple[bool, Answers | None]:
    """
    Run solve() on every example and compare with the expected answers, then run
    it on the real input. The real input is skipped while an example fails, unless
    force_real is set. Returns (examples_ok, real_answers or None).
    """
    header(puzzle, "check")
    if not puzzle.solution.exists():
        print(red(f"  ✗ Not found: {puzzle.rel(puzzle.solution)} (run: make today)"))
        return False, None

    expected_by_example = load_expected(puzzle)
    examples = puzzle.examples()
    if not examples:
        print(dim(f"  no examples yet, paste one into inputs/{puzzle.year}/day{puzzle.day:02d}.example.txt"))

    examples_ok = True
    for path in examples:
        name = example_name(path)
        text = path.read_text()
        if not text.strip():
            print(dim(f"  {name:<10} empty, paste the example into {puzzle.rel(path)}"))
            continue
        try:
            answers, _ = run_solve(puzzle, text)
        except Exception:
            print(red(f"  ✗ {name}: solve() raised\n"))
            traceback.print_exc()
            examples_ok = False
            continue
        expected = expected_by_example.get(name, {})
        for part, got in enumerate(answers, start=1):
            want = str(expected.get(f"part{part}", "")).strip()
            label = dim(f"{name:<10} part {part}")
            shown = gold(got) if got else dim("(empty)")
            if not want:
                print(f"  {label}  {shown}  {dim('(no expected answer)')}")
            elif got == want:
                print(f"  {label}  {shown}  {green('✓')}")
            else:
                print(f"  {label}  {shown}  {red(f'✗ expected {want}')}")
                examples_ok = False

    print()
    if not examples_ok and not force_real:
        print(red("  ✗ Examples failing, real input skipped"))
        return False, None
    if not puzzle.input.exists():
        print(dim(f"  no real input at {puzzle.rel(puzzle.input)} (run: make today)"))
        return examples_ok, None

    try:
        answers, elapsed_ms = run_solve(puzzle, puzzle.input.read_text())
    except Exception:
        print(red("  ✗ solve() raised on the real input\n"))
        traceback.print_exc()
        return examples_ok, None
    for part, got in enumerate(answers, start=1):
        label = dim(f"{'input':<10} part {part}")
        print(f"  {label}  {gold(got) if got else dim('(empty)')}")
    print(f"\n  {green('✓')} {dim(f'{elapsed_ms:.1f} ms')}")
    return examples_ok, answers


# ── watch ─────────────────────────────────────────────────────────────────────

def watched_files(puzzle: Puzzle) -> dict[Path, int]:
    """Modification times of everything that can change the outcome of a check."""
    files = [
        *puzzle.solution_dir.glob("*.py"),
        *puzzle.solution_dir.parent.glob("*.py"),  # shared modules of the year
        *puzzle.examples(),
        puzzle.answers,
        puzzle.input,
    ]
    return {path: path.stat().st_mtime_ns for path in files if path.exists()}


def watch(puzzle: Puzzle) -> None:
    """Re-run check in a subprocess on every save; a new save stops a slow run."""
    command = [sys.executable, str(Path(__file__).resolve()), "--root", str(puzzle.root),
               "check", str(puzzle.year), str(puzzle.day)]
    process: subprocess.Popen | None = None
    last_seen: dict[Path, int] | None = None
    try:
        while True:
            current = watched_files(puzzle)
            if current != last_seen:
                last_seen = current
                if process and process.poll() is None:
                    process.terminate()
                    process.wait()
                if sys.stdout.isatty():
                    print("\033[2J\033[H", end="")
                print(dim(f"  watching {puzzle.rel(puzzle.solution_dir)}, Ctrl+C to stop"), flush=True)
                process = subprocess.Popen(command)
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        if process and process.poll() is None:
            process.terminate()
        print()


# ── today ─────────────────────────────────────────────────────────────────────

def fetch_with_aocd(puzzle: Puzzle) -> str:
    from aocd import get_data  # imported lazily: check and watch work without aocd
    return get_data(year=puzzle.year, day=puzzle.day, block=True)


def today(puzzle: Puzzle, fetch: Callable[[Puzzle], str] = fetch_with_aocd) -> None:
    """Create everything needed to start solving. Never overwrites existing files."""
    header(puzzle, "today")

    template_dir = puzzle.root / "solutions" / "template"
    puzzle.solution_dir.mkdir(parents=True, exist_ok=True)
    for name in ("solution.py", "meta.json"):
        target = puzzle.solution_dir / name
        if target.exists():
            print(dim(f"  exists     {puzzle.rel(target)}"))
            continue
        content = (template_dir / name).read_text()
        if name == "solution.py":
            content = content.replace("Day XX", f"Day {puzzle.day:02d}", 1)
            content = content.replace("Year: XXXX", f"Year: {puzzle.year}", 1)
        target.write_text(content)
        print(f"  {green('created')}    {puzzle.rel(target)}")

    puzzle.input_dir.mkdir(parents=True, exist_ok=True)
    if puzzle.input.exists():
        print(dim(f"  exists     {puzzle.rel(puzzle.input)}"))
    else:
        print(dim("  downloading input (waits for the unlock if needed)..."), flush=True)
        try:
            data = fetch(puzzle)
        except Exception as error:
            print(red(f"  ✗ Could not download the input: {error}"))
            print(dim("    Set AOC_SESSION or ~/.config/aocd/token to your adventofcode.com session cookie,"))
            print(dim(f"    or save the input yourself as {puzzle.rel(puzzle.input)}"))
        else:
            puzzle.input.write_text(data if data.endswith("\n") else data + "\n")
            print(f"  {green('downloaded')} {puzzle.rel(puzzle.input)}  {dim(f'({len(data.splitlines())} lines)')}")

    if not puzzle.examples():
        example = puzzle.input_dir / f"day{puzzle.day:02d}.example.txt"
        example.write_text("")
        print(f"  {green('created')}    {puzzle.rel(example)}  {dim('(paste the example here)')}")
    if not puzzle.answers.exists():
        puzzle.answers.write_text(json.dumps({"example": {"part1": "", "part2": ""}}, indent=2) + "\n")
        print(f"  {green('created')}    {puzzle.rel(puzzle.answers)}  {dim('(fill in the expected answers)')}")

    print()
    print(f"  {gold(puzzle.url)}")
    print(dim(f"  next: make watch YEAR={puzzle.year} DAY={puzzle.day:02d}"))
    print()


# ── submit ────────────────────────────────────────────────────────────────────

def submit_with_aocd(puzzle: Puzzle, part: int, answer: str) -> None:
    from aocd import submit as aocd_submit  # imported lazily: check and watch work without aocd
    aocd_submit(answer, part="ab"[part - 1], day=puzzle.day, year=puzzle.year)


def submit(
    puzzle: Puzzle,
    part: int,
    force: bool = False,
    confirm: Callable[[str], str] = input,
    send: Callable[[Puzzle, int, str], None] = submit_with_aocd,
) -> bool:
    """Check the examples, run the real input and submit one part after a y/N prompt."""
    examples_ok, real = check(puzzle, force_real=force)
    print()
    if real is None:
        print(red("  ✗ Not submitting: no answer for the real input" + ("" if force else " (--force skips the example check)")))
        return False
    answer = real[part - 1]
    if not answer:
        print(red(f"  ✗ Not submitting: part {part} returned an empty answer"))
        return False
    if not examples_ok:
        print(red("  ! Examples are failing, submitting anyway because of --force"))
    try:
        reply = confirm(f"  Submit {bold(answer)} for {puzzle.year} day {puzzle.day} part {part}? [y/N] ")
    except EOFError:
        reply = ""
    if reply.strip().lower() not in ("y", "yes"):
        print(dim("  not submitted"))
        return False
    send(puzzle, part, answer)
    return True


# ── CLI ───────────────────────────────────────────────────────────────────────

def resolve_puzzle(year: int | None, day: int | None, root: Path) -> Puzzle:
    if year is None and day is None:
        current = today_puzzle()
        if current is None:
            sys.exit(red("  ✗ No puzzle today, pass YEAR and DAY (for example: 2025 1)"))
        year, day = current
    elif year is None or day is None:
        sys.exit(red("  ✗ Pass both YEAR and DAY, or neither for today's puzzle"))
    if year < 2015 or not 1 <= day <= 25:
        sys.exit(red(f"  ✗ Not an Advent of Code puzzle: {year} day {day}"))
    return Puzzle(year, day, root)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Daily Advent of Code workflow: today, check, watch, submit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, description in [
        ("today", "scaffold the solution, download the input, create example files"),
        ("check", "run solve() on the examples, then on the real input"),
        ("watch", "re-run check every time a file of the day is saved"),
        ("submit", "run on the real input and submit one part after confirmation"),
    ]:
        command = commands.add_parser(name, help=description)
        command.add_argument("year", type=int, nargs="?")
        command.add_argument("day", type=int, nargs="?")
        if name == "submit":
            command.add_argument("--part", type=int, choices=(1, 2), required=True)
            command.add_argument("--force", action="store_true",
                                 help="submit even when an example fails")
    args = parser.parse_args()
    puzzle = resolve_puzzle(args.year, args.day, args.root.resolve())

    if args.command == "today":
        today(puzzle)
    elif args.command == "check":
        examples_ok, real = check(puzzle)
        print()
        sys.exit(0 if examples_ok else 1)
    elif args.command == "watch":
        watch(puzzle)
    elif args.command == "submit":
        sys.exit(0 if submit(puzzle, args.part, force=args.force) else 1)


if __name__ == "__main__":
    main()
