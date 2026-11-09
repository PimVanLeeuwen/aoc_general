#!/usr/bin/env python3
"""
Run ALL Advent of Code solutions in a fixed-frame terminal UI.

Usage:
    python3 run_all.py                  # run everything
    python3 run_all.py --year 2024      # run one year only
    python3 run_all.py --timeout 30     # 30s timeout per solution
    python3 run_all.py --pause 0.5      # delay between days (for timelapse)
"""

import argparse
import dataclasses
import importlib.util
import json
import signal
import sys
import time
import traceback
from pathlib import Path

# ── ANSI helpers ─────────────────────────────────────────────────────────────

ESC = "\033"


def _c(code: str, text: str) -> str:
    return f"{ESC}[{code}m{text}{ESC}[0m"


def gold(t): return _c("93", t)
def green(t): return _c("92", t)
def red(t): return _c("91", t)
def dim(t): return _c("2", t)
def bold(t): return _c("1", t)
def cyan(t): return _c("96", t)
def magenta(t): return _c("95", t)
def white(t): return _c("97", t)


def move(row, col):
    """Move cursor to (row, col) — 1-based."""
    sys.stdout.write(f"{ESC}[{row};{col}H")


def clear_screen():
    sys.stdout.write(f"{ESC}[2J")
    sys.stdout.write(f"{ESC}[H")


def hide_cursor():
    sys.stdout.write(f"{ESC}[?25l")


def show_cursor():
    sys.stdout.write(f"{ESC}[?25h")


# ── Data ─────────────────────────────────────────────────────────────────────

W = 62   # inner width (characters between box borders)
H = 36   # total frame height


@dataclasses.dataclass
class DayResult:
    year: int
    day: int
    title: str
    part1: str
    part2: str
    elapsed_ms: float
    stars: int
    status: str  # "ok", "error", "timeout", "missing"
    error_msg: str = ""


# ── Solution runner ──────────────────────────────────────────────────────────


def find_input(year: int, day: int) -> Path | None:
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
        return None, path
    year_dir = str(Path(f"solutions/{year}").resolve())
    if year_dir not in sys.path:
        sys.path.insert(0, year_dir)
    spec = importlib.util.spec_from_file_location("solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def load_meta(year: int, day: int) -> dict:
    path = Path(f"solutions/{year}/day{day:02d}/meta.json")
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def discover_days(year_filter: int | None = None):
    years = [year_filter] if year_filter else range(2015, 2026)
    for year in years:
        year_dir = Path(f"solutions/{year}")
        if not year_dir.exists():
            continue
        days = sorted(
            int(d.name[3:]) for d in year_dir.iterdir()
            if d.is_dir() and d.name.startswith("day")
        )
        for day in days:
            yield year, day


class SolveTimeout(Exception):
    pass


def _alarm_handler(signum, frame):
    raise SolveTimeout()


def run_day(year: int, day: int, timeout: int) -> DayResult:
    meta = load_meta(year, day)
    title = meta.get("title", "???")
    stars = meta.get("stars", 0)

    input_path = find_input(year, day)
    if not input_path:
        return DayResult(year, day, title, "", "", 0, stars, "missing", "No input")

    puzzle_input = input_path.read_text()
    module, path = load_module(year, day)
    if module is None:
        return DayResult(year, day, title, "", "", 0, stars, "missing", "No solution")

    if not hasattr(module, "solve"):
        return DayResult(year, day, title, "", "", 0, stars, "error", "No solve()")

    old_handler = signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(timeout)
    try:
        start = time.perf_counter()
        result = module.solve(puzzle_input)
        elapsed_ms = (time.perf_counter() - start) * 1000
    except SolveTimeout:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
        return DayResult(year, day, title, "", "", timeout * 1000, stars, "timeout")
    except Exception:
        elapsed_ms = (time.perf_counter() - start) * 1000
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
        tb = traceback.format_exc().splitlines()[-1]
        return DayResult(year, day, title, "", "", elapsed_ms, stars, "error", tb)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

    if isinstance(result, (tuple, list)):
        part1 = str(result[0]) if len(result) > 0 else ""
        part2 = str(result[1]) if len(result) > 1 else ""
    else:
        part1, part2 = str(result), ""

    return DayResult(year, day, title, part1, part2, elapsed_ms, stars, "ok")


# ── Formatting helpers ───────────────────────────────────────────────────────


def fmt_duration(ms: float) -> str:
    if ms >= 60_000:
        return f"{int(ms // 60_000)}m {(ms % 60_000) / 1000:.1f}s"
    elif ms >= 1000:
        return f"{ms / 1000:.1f}s"
    else:
        return f"{ms:.0f}ms"


def trunc(s: str, maxlen: int) -> str:
    return s[:maxlen - 3] + "..." if len(s) > maxlen else s


def progress_bar(fraction: float, width: int) -> str:
    filled = int(fraction * width)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    return bar


# ── Frame renderer ───────────────────────────────────────────────────────────


class Display:
    """Fixed-frame terminal UI. Redraws entire screen on each update."""

    HISTORY_ROWS = 18  # number of result lines visible in the scroll area

    def __init__(self, total_days: int, total_years: int):
        self.total_days = total_days
        self.total_years = total_years
        self.results: list[DayResult] = []
        self.current_year = None
        self.year_results: list[DayResult] = []
        self.running: tuple[int, int, str] | None = None  # (year, day, title)
        self.start_time = time.time()
        self.year_times: dict[int, float] = {}  # year -> total ms

    @property
    def solved(self):
        return sum(1 for r in self.results if r.status == "ok")

    @property
    def total_stars(self):
        return sum(r.stars for r in self.results if r.status == "ok")

    @property
    def max_stars(self):
        return self.total_days * 2

    @property
    def total_ms(self):
        return sum(r.elapsed_ms for r in self.results)

    @property
    def errors(self):
        return sum(1 for r in self.results if r.status in ("error", "timeout"))

    @property
    def elapsed_wall(self):
        return time.time() - self.start_time

    def add_result(self, result: DayResult):
        if result.year != self.current_year:
            if self.current_year is not None:
                self.year_times[self.current_year] = sum(
                    r.elapsed_ms for r in self.year_results
                )
            self.current_year = result.year
            self.year_results = []
        self.year_results.append(result)
        self.results.append(result)
        self.running = None

    def set_running(self, year: int, day: int, title: str):
        self.running = (year, day, title)

    def finalize(self):
        if self.current_year is not None:
            self.year_times[self.current_year] = sum(
                r.elapsed_ms for r in self.year_results
            )

    def render(self):
        lines = []

        def add(text=""):
            lines.append(text)

        bdr = dim("│")
        w = W

        def padline(ansi_text, vis_len):
            return f"{bdr}{ansi_text}{' ' * max(0, w - vis_len)}{bdr}"

        # ── Top border ───────────────────────────────────────────────
        add(dim("┌" + "─" * w + "┐"))

        # ── Title ────────────────────────────────────────────────────
        title = "Advent of Code  ·  Complete Run"
        pad = w - len(title)
        add(f"{bdr}{' ' * (pad // 2)}{bold(title)}{' ' * (pad - pad // 2)}{bdr}")

        # ── Progress bar ─────────────────────────────────────────────
        add(dim("├" + "─" * w + "┤"))
        frac = len(self.results) / self.total_days if self.total_days else 0
        pct = f"{frac * 100:5.1f}%"
        count = f"{len(self.results):>3d}/{self.total_days}"
        bar_w = w - len(pct) - len(count) - 8  # 2+2+2+2 spacing
        bar = progress_bar(frac, bar_w)
        row_vis = f"  {bar}  {pct}  {count}  "
        row_ansi = f"  {green(bar)}  {bold(pct)}  {dim(count)}  "
        add(padline(row_ansi, len(row_vis)))

        # ── Stats row 1 ──────────────────────────────────────────────
        wall = fmt_duration(self.elapsed_wall * 1000)
        solve_t = fmt_duration(self.total_ms)
        stars_str = f"{self.total_stars}/{self.max_stars}"
        err_str = str(self.errors)

        r1_vis = f"  Elapsed  {wall:<20s}Solve time  {solve_t}"
        r1 = f"  Elapsed  {bold(wall)}{' ' * max(0, 20 - len(wall))}Solve time  {bold(solve_t)}"
        add(padline(r1, len(r1_vis)))

        r2_vis = f"  Stars  {stars_str:<20s}Solved  {str(self.solved):<14s}Err  {self.errors}"
        r2 = f"  Stars  {gold(stars_str)}{' ' * max(0, 20 - len(stars_str))}Solved  {bold(str(self.solved))}{' ' * max(0, 14 - len(str(self.solved)))}Err  {red(err_str) if self.errors else dim(err_str)}"
        add(padline(r2, len(r2_vis)))

        # ── Year progress bar ────────────────────────────────────────
        add(dim("├" + "─" * w + "┤"))

        if self.current_year:
            yr = self.current_year
            yr_done = len(self.year_results)
            yr_total = sum(1 for y, _ in discover_days(yr))
            yr_frac = yr_done / yr_total if yr_total else 0
            yr_bar_w = w - 30
            yr_bar = progress_bar(yr_frac, yr_bar_w)
            yr_count = f"{yr_done:>2d}/{yr_total}"
            yr_time = fmt_duration(sum(r.elapsed_ms for r in self.year_results))
            yr_line = f"  {gold('*')} {bold(str(yr))}  {green(yr_bar)}  {yr_count}  {dim(yr_time)}"
            yr_line_vis = f"  * {yr}  {yr_bar}  {yr_count}  {yr_time}"
            add(padline(yr_line, len(yr_line_vis)))
        else:
            add(f"{bdr}{' ' * w}{bdr}")

        # ── Results history ──────────────────────────────────────────
        add(dim("├" + "─" * w + "┤"))

        history_lines = []
        for r in self.results:
            history_lines.append(self._fmt_result(r))

        # Add "running" line
        if self.running:
            ry, rd, rt = self.running
            spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
            spin_ch = spinner[int(time.time() * 8) % len(spinner)]
            rt = trunc(rt, 28)
            line = f"  {gold(spin_ch)} {ry} Day {rd:02d}  {cyan(rt)}"
            line_vis = f"  {spin_ch} {ry} Day {rd:02d}  {rt}"
            pad = w - len(line_vis)
            history_lines.append(f"{line}{' ' * max(0, pad)}")

        # Show last N lines
        visible = history_lines[-self.HISTORY_ROWS:]
        for hl in visible:
            add(f"{bdr}{hl}{bdr}")

        # Pad remaining rows
        for _ in range(self.HISTORY_ROWS - len(visible)):
            add(f"{bdr}{' ' * w}{bdr}")

        # ── Bottom stats ─────────────────────────────────────────────
        add(dim("├" + "─" * w + "┤"))

        ok_results = [r for r in self.results if r.status == "ok"]
        if ok_results:
            fastest = min(ok_results, key=lambda r: r.elapsed_ms)
            slowest = max(ok_results, key=lambda r: r.elapsed_ms)
            fl = f"Fastest  {fastest.year}/{fastest.day:02d} {trunc(fastest.title, 16)} {green(fmt_duration(fastest.elapsed_ms))}"
            fl_vis = f"Fastest  {fastest.year}/{fastest.day:02d} {trunc(fastest.title, 16)} {fmt_duration(fastest.elapsed_ms)}"
            sl = f"Slowest  {slowest.year}/{slowest.day:02d} {trunc(slowest.title, 16)} {red(fmt_duration(slowest.elapsed_ms))}"
            sl_vis = f"Slowest  {slowest.year}/{slowest.day:02d} {trunc(slowest.title, 16)} {fmt_duration(slowest.elapsed_ms)}"
            add(f"{bdr}  {fl}{' ' * max(0, w - len(fl_vis) - 2)}{bdr}")
            add(f"{bdr}  {sl}{' ' * max(0, w - len(sl_vis) - 2)}{bdr}")
        else:
            add(f"{bdr}{' ' * w}{bdr}")
            add(f"{bdr}{' ' * w}{bdr}")

        # ── Bottom border ────────────────────────────────────────────
        add(dim("└" + "─" * w + "┘"))

        # ── Write to screen ──────────────────────────────────────────
        move(1, 1)
        sys.stdout.write("\n".join(lines))
        sys.stdout.flush()

    def _fmt_result(self, r: DayResult) -> str:
        """Format a single result as one fixed-width line (exactly W visible chars)."""
        w = W
        title = trunc(r.title, 22)

        if r.status == "ok":
            stars = gold("**") if r.stars >= 2 else (gold("*") + dim("*") if r.stars == 1 else dim(".."))
            timing = fmt_duration(r.elapsed_ms)
            p1 = trunc(r.part1, 18)
            left = f"  {stars} {r.year} Day {r.day:02d}  {title}"
            left_vis = f"  ** {r.year} Day {r.day:02d}  {title}"
            right_vis = f"{p1}  {timing}"
            right = f"{dim(p1)}  {green(timing)}"
        elif r.status == "timeout":
            left = f"  {dim('..')} {r.year} Day {r.day:02d}  {title}"
            left_vis = f"  .. {r.year} Day {r.day:02d}  {title}"
            right_vis = "TIMEOUT"
            right = red("TIMEOUT")
        elif r.status == "error":
            left = f"  {dim('..')} {r.year} Day {r.day:02d}  {title}"
            left_vis = f"  .. {r.year} Day {r.day:02d}  {title}"
            right_vis = "ERROR"
            right = red("ERROR")
        else:
            left = f"  {dim('--')} {r.year} Day {r.day:02d}  {dim(title)}"
            left_vis = f"  -- {r.year} Day {r.day:02d}  {title}"
            right_vis = "SKIP"
            right = dim("SKIP")

        gap = w - len(left_vis) - len(right_vis)
        return f"{left}{' ' * max(1, gap)}{right}"


# ── Completion screen ────────────────────────────────────────────────────────


def render_final(display: Display):
    """Replace the running display with a final summary screen."""
    lines = []
    bdr = dim("│")
    w = W

    def add(text=""):
        lines.append(text)

    add(dim("┌" + "─" * w + "┐"))

    # Title
    title = "Advent of Code  ·  Complete!"
    pad = w - len(title)
    add(f"{bdr}{' ' * (pad // 2)}{gold(title)}{' ' * (pad - pad // 2)}{bdr}")

    add(dim("├" + "─" * w + "┤"))

    # Full progress bar
    bar = progress_bar(1.0, w - 12)
    add(f"{bdr}  {green(bar)}  {bold('100.0%')}  {bdr}")

    add(dim("├" + "─" * w + "┤"))

    # Summary stats
    ok = [r for r in display.results if r.status == "ok"]

    def row(label, value):
        content = f"  {label:<16s}{value}"
        p = w - len(content)
        add(f"{bdr}{content}{' ' * max(0, p)}{bdr}")

    row("Days solved:", f"{display.solved} / {display.total_days}")
    row("Stars:", f"{display.total_stars} / {display.max_stars}")
    row("Total solve:", fmt_duration(display.total_ms))
    row("Wall time:", fmt_duration(display.elapsed_wall * 1000))
    row("Errors:", str(display.errors))

    add(f"{bdr}{' ' * w}{bdr}")

    # Per-year breakdown
    add(dim("├" + "─" * w + "┤"))
    header = "  Year    Days   Stars    Time"
    add(f"{bdr}{header:<{w}s}{bdr}")
    add(dim("├" + "─" * w + "┤"))

    years = sorted(display.year_times.keys())
    for yr in years:
        yr_results = [r for r in display.results if r.year == yr]
        yr_solved = sum(1 for r in yr_results if r.status == "ok")
        yr_total = len(yr_results)
        yr_stars = sum(r.stars for r in yr_results if r.status == "ok")
        yr_max = yr_total * 2
        yr_time = fmt_duration(display.year_times[yr])
        line = f"  {yr}    {yr_solved:>2d}/{yr_total:<2d}   {yr_stars:>2d}/{yr_max:<3d}   {yr_time:>8s}"
        add(f"{bdr}{line:<{w}s}{bdr}")

    # Pad to fill frame
    used = len(lines)
    target = H - 5  # leave room for fastest/slowest + border
    for _ in range(max(0, target - used)):
        add(f"{bdr}{' ' * w}{bdr}")

    # Fastest / slowest
    add(dim("├" + "─" * w + "┤"))
    if ok:
        fastest = min(ok, key=lambda r: r.elapsed_ms)
        slowest = max(ok, key=lambda r: r.elapsed_ms)
        fl = f"  Fastest  {fastest.year}/{fastest.day:02d} {trunc(fastest.title, 20)}  {green(fmt_duration(fastest.elapsed_ms))}"
        fl_vis = f"  Fastest  {fastest.year}/{fastest.day:02d} {trunc(fastest.title, 20)}  {fmt_duration(fastest.elapsed_ms)}"
        sl = f"  Slowest  {slowest.year}/{slowest.day:02d} {trunc(slowest.title, 20)}  {red(fmt_duration(slowest.elapsed_ms))}"
        sl_vis = f"  Slowest  {slowest.year}/{slowest.day:02d} {trunc(slowest.title, 20)}  {fmt_duration(slowest.elapsed_ms)}"
        add(f"{bdr}{fl}{' ' * max(0, w - len(fl_vis))}{bdr}")
        add(f"{bdr}{sl}{' ' * max(0, w - len(sl_vis))}{bdr}")
    else:
        add(f"{bdr}{' ' * w}{bdr}")
        add(f"{bdr}{' ' * w}{bdr}")

    add(dim("└" + "─" * w + "┘"))

    move(1, 1)
    sys.stdout.write("\n".join(lines))
    sys.stdout.flush()


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Run all AoC solutions")
    parser.add_argument("--year", type=int, help="Run only this year")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds (default: 60)")
    parser.add_argument("--pause", type=float, default=0.3, help="Delay between days (default: 0.3)")
    args = parser.parse_args()

    days = list(discover_days(args.year))
    total = len(days)
    years = sorted(set(y for y, _ in days))

    display = Display(total, len(years))

    hide_cursor()
    clear_screen()

    try:
        display.render()

        for year, day in days:
            meta = load_meta(year, day)
            title = meta.get("title", "???")
            display.set_running(year, day, title)
            display.render()

            result = run_day(year, day, args.timeout)
            display.add_result(result)
            display.render()

            time.sleep(args.pause)

        display.finalize()
        render_final(display)

        # Keep final screen visible
        move(H + 1, 1)
        print()
    finally:
        show_cursor()


if __name__ == "__main__":
    main()
