"""
Day 17 - Reservoir Research
Year: 2018

Simulate water flowing from x=500,y=0 through a clay-walled underground scan.
Part 1: all tiles reachable by water (flowing | settled) within y bounds.
Part 2: tiles of retained (settled) water after flow stops.
"""

import re
import sys


def parse(puzzle_input: str) -> set:
    clay = set()
    for line in puzzle_input.strip().splitlines():
        a, b, c = map(int, re.findall(r'\d+', line))
        if line.startswith('x'):
            for y in range(b, c + 1):
                clay.add((a, y))
        else:
            for x in range(b, c + 1):
                clay.add((x, a))
    return clay


def simulate(clay: set):
    min_y = min(y for _, y in clay)
    max_y = max(y for _, y in clay)
    settled: set = set()
    flowing: set = set()
    sys.setrecursionlimit(10000)

    def down(x, y):
        if y > max_y:
            return False
        if (x, y) in clay or (x, y) in settled:
            return True
        if (x, y) in flowing:
            return False
        flowing.add((x, y))
        if not down(x, y + 1):
            return False
        return spread(x, y)

    def spread(x, y):
        lx, lw = scan(x, y, -1)
        rx, rw = scan(x, y, +1)
        if lw and rw:
            for nx in range(lx, rx + 1):
                settled.add((nx, y))
                flowing.discard((nx, y))
            return True
        return False

    def scan(x, y, dx):
        cx = x
        while True:
            if (cx + dx, y) in clay:
                return cx, True
            cx += dx
            flowing.add((cx, y))
            if (cx, y + 1) not in clay and (cx, y + 1) not in settled:
                if not down(cx, y + 1):
                    return cx, False

    down(500, 0)
    return flowing, settled, min_y, max_y


def solve(puzzle_input: str) -> tuple[str, str]:
    clay = parse(puzzle_input)
    flowing, settled, min_y, max_y = simulate(clay)
    part1 = sum(1 for _, y in flowing | settled if min_y <= y <= max_y)
    part2 = sum(1 for _, y in settled if min_y <= y <= max_y)
    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    clay = parse(puzzle_input)
    flowing, settled, min_y, max_y = simulate(clay)

    all_x = {x for x, _ in clay} | {x for x, _ in flowing} | {x for x, _ in settled}
    min_x, max_x = min(all_x) - 1, max(all_x) + 1

    COLORS = {
        '#': '#8B6914',
        '~': '#1E6FCC',
        '|': '#7EC8E3',
        '.': '#1a1a2e',
        '+': '#ffffff',
    }

    def render(include_water=False):
        cells = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                if (x, y) in clay:
                    row.append('#')
                elif include_water and (x, y) in settled:
                    row.append('~')
                elif include_water and (x, y) in flowing:
                    row.append('|')
                else:
                    row.append('.')
            cells.append(row)
        return cells

    yield {"type": "grid", "cells": render(False), "colors": COLORS, "delay": 1000}
    yield {"type": "grid", "cells": render(True),  "colors": COLORS, "delay": 2000}

    part1 = sum(1 for _, y in flowing | settled if min_y <= y <= max_y)
    part2 = sum(1 for _, y in settled if min_y <= y <= max_y)
    yield {
        "type": "text",
        "lines": [
            "Reservoir Research",
            "",
            f"y range     : {min_y} … {max_y}",
            f"Clay tiles  : {len(clay)}",
            f"Reachable   : {part1}  (Part 1)",
            f"Settled (~) : {part2}  (Part 2)",
        ],
        "delay": 4000,
    }
