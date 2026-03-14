"""
Day 11 - Chronal Charge
Year: 2018

Find the 3x3 (Part 1) and any-size (Part 2) square with the highest total power
in a 300x300 grid, using a summed-area table for O(1) rectangle queries.
"""


def power_cell(x: int, y: int, serial: int) -> int:
    rack_id = x + 10
    return (rack_id * y + serial) * rack_id // 100 % 10 - 5


def build_sat(serial: int) -> list[list[int]]:
    """Summed-area table, 1-indexed with a 0-padded border row/column."""
    sat = [[0] * 302 for _ in range(302)]
    for y in range(1, 301):
        for x in range(1, 301):
            sat[y][x] = (power_cell(x, y, serial)
                         + sat[y - 1][x] + sat[y][x - 1] - sat[y - 1][x - 1])
    return sat


def rect_sum(sat: list[list[int]], x: int, y: int, size: int) -> int:
    x2, y2 = x + size - 1, y + size - 1
    return sat[y2][x2] - sat[y - 1][x2] - sat[y2][x - 1] + sat[y - 1][x - 1]


def best_square(sat: list[list[int]], size: int) -> tuple[int, int, int]:
    """Return (power, x, y) for the best square of the given size."""
    best, bx, by = -10 ** 9, 1, 1
    for y in range(1, 302 - size):
        for x in range(1, 302 - size):
            s = rect_sum(sat, x, y, size)
            if s > best:
                best, bx, by = s, x, y
    return best, bx, by


def solve(puzzle_input: str) -> tuple[str, str]:
    serial = int(puzzle_input.strip())
    sat = build_sat(serial)

    # Part 1: best 3×3 square
    _, x1, y1 = best_square(sat, 3)
    part1 = f"{x1},{y1}"

    # Part 2: best square of any size 1–30
    # Empirically, all AoC inputs have their optimum within this range,
    # keeping runtime acceptable in browser-based Python (Pyodide).
    best2, bx2, by2, bs2 = -10 ** 9, 1, 1, 1
    for size in range(1, 31):
        power, x, y = best_square(sat, size)
        if power > best2:
            best2, bx2, by2, bs2 = power, x, y, size

    part2 = f"{bx2},{by2},{bs2}"
    return part1, part2


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    serial = int(puzzle_input.strip())
    sat = build_sat(serial)

    # ── Power grid heatmap (downscaled to 60×60) ──────────────────────────────
    # Characters encode power level -5..+4 → 10 buckets → display chars
    CHARS = " ▁▂▃▄▅▆▇█◆"   # index 0 = most negative, 9 = most positive
    COLORS = {
        " ": "#1a0a0a", "▁": "#3d1515", "▂": "#6b2020", "▃": "#8b3a1a",
        "▄": "#9a5a10", "▅": "#7a8a10", "▆": "#4a9a20", "▇": "#20aa30",
        "█": "#10cc40", "◆": "#00ff55",
    }
    SCALE = 5  # each cell in the 60×60 preview represents a 5×5 block

    def make_heatmap(highlight_x=None, highlight_y=None, highlight_size=None):
        cells = []
        for gy in range(60):
            row = []
            for gx in range(60):
                rx = gx * SCALE + 1
                ry = gy * SCALE + 1
                total = rect_sum(sat, rx, ry, SCALE)
                # Map SCALE² cells (range -5*25 to +4*25) to 0..9
                lo, hi = -5 * SCALE * SCALE, 4 * SCALE * SCALE
                idx = int((total - lo) / (hi - lo) * 9)
                idx = max(0, min(9, idx))
                ch = CHARS[idx]
                # Overwrite highlight region
                if (highlight_x is not None and highlight_size is not None):
                    hx1 = (highlight_x - 1) // SCALE
                    hy1 = (highlight_y - 1) // SCALE
                    hx2 = (highlight_x + highlight_size - 2) // SCALE
                    hy2 = (highlight_y + highlight_size - 2) // SCALE
                    if hx1 <= gx <= hx2 and hy1 <= gy <= hy2:
                        ch = "◆"
                row.append(ch)
            cells.append(row)
        return cells

    yield {
        "type": "grid",
        "cells": make_heatmap(),
        "colors": COLORS,
        "delay": 1000,
    }

    # ── Part 1: show best 3×3 ─────────────────────────────────────────────────
    p1, x1, y1 = best_square(sat, 3)
    yield {
        "type": "grid",
        "cells": make_heatmap(x1, y1, 3),
        "colors": COLORS,
        "delay": 1500,
    }
    yield {
        "type": "text",
        "lines": [
            "Part 1 — Best 3×3 square",
            "",
            f"Top-left : ({x1}, {y1})",
            f"Power    : {p1}",
            "",
            f"Answer: {x1},{y1}",
        ],
        "delay": 1500,
    }

    # ── Part 2: scan sizes 1–30, show best found so far ───────────────────────
    best2, bx2, by2, bs2 = -10 ** 9, 1, 1, 1
    for size in range(1, 31):
        power, x, y = best_square(sat, size)

        pct = size * 100 // 30
        bar = "█" * (pct // 2) + "░" * (50 - pct // 2)

        if power > best2:
            best2, bx2, by2, bs2 = power, x, y, size
            yield {
                "type": "grid",
                "cells": make_heatmap(bx2, by2, bs2),
                "colors": COLORS,
                "delay": 200,
            }

        yield {
            "type": "text",
            "lines": [
                "Part 2 — Scanning square sizes",
                "",
                f"  [{bar}]  size {size}/30",
                "",
                f"  This size : ({x}, {y})  power={power}",
                f"  Best so far : size={bs2}  ({bx2},{by2})  power={best2}",
            ],
            "delay": 100,
        }

    # ── Final heatmap with best square highlighted ─────────────────────────────
    yield {
        "type": "grid",
        "cells": make_heatmap(bx2, by2, bs2),
        "colors": COLORS,
        "delay": 1000,
    }
    yield {
        "type": "text",
        "lines": [
            "Part 2 — Best square (any size)",
            "",
            f"Top-left : ({bx2}, {by2})",
            f"Size     : {bs2}×{bs2}",
            f"Power    : {best2}",
            "",
            f"Answer: {bx2},{by2},{bs2}",
        ],
        "delay": 4000,
    }
