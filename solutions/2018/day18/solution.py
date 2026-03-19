"""
Day 18 - Settlers of The North Pole
Year: 2018

Cellular automaton on a 50x50 grid of open (.), trees (|), and lumberyards (#).
Part 1: resource value (trees * lumberyards) after 10 minutes.
Part 2: resource value after 1,000,000,000 minutes via cycle detection.
"""


def step(grid):
    rows, cols = len(grid), len(grid[0])
    new = []
    for r in range(rows):
        row = []
        for c in range(cols):
            nbrs = [grid[r+dr][c+dc]
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                    if (dr, dc) != (0, 0) and 0 <= r+dr < rows and 0 <= c+dc < cols]
            cur = grid[r][c]
            if cur == '.' and nbrs.count('|') >= 3:
                row.append('|')
            elif cur == '|' and nbrs.count('#') >= 3:
                row.append('#')
            elif cur == '#' and not (nbrs.count('#') >= 1 and nbrs.count('|') >= 1):
                row.append('.')
            else:
                row.append(cur)
        new.append(row)
    return new


def resource(grid):
    flat = [c for row in grid for c in row]
    return flat.count('|') * flat.count('#')


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = [list(line) for line in puzzle_input.strip().splitlines()]

    # Part 1: 10 steps
    g = [row[:] for row in grid]
    for _ in range(10):
        g = step(g)
    part1 = resource(g)

    # Part 2: cycle detection
    g = [row[:] for row in grid]
    seen = {}
    target = 1_000_000_000
    for i in range(target):
        key = tuple(c for row in g for c in row)
        if key in seen:
            cycle_start = seen[key]
            cycle_len = i - cycle_start
            remaining = (target - i) % cycle_len
            for _ in range(remaining):
                g = step(g)
            break
        seen[key] = i
        g = step(g)
    part2 = resource(g)

    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    COLORS = {'.': '#1a2e1a', '|': '#00aa33', '#': '#8B6914'}

    grid = [list(line) for line in puzzle_input.strip().splitlines()]

    yield {"type": "grid", "cells": grid, "colors": COLORS, "delay": 400}

    seen = {}
    for i in range(1, 600):
        key = tuple(c for row in grid for c in row)
        if key in seen:
            cycle_len = i - seen[key]
            yield {
                "type": "text",
                "lines": [
                    f"Cycle detected at minute {i}",
                    f"Cycle length: {cycle_len}",
                    "",
                    f"Part 1 (min 10)  : already shown",
                    f"Part 2 (min 1B)  : extrapolated",
                ],
                "delay": 3000,
            }
            break
        seen[key] = i
        grid = step(grid)
        delay = 300 if i <= 20 else 80
        yield {"type": "grid", "cells": grid, "colors": COLORS, "delay": delay}
        if i == 10:
            yield {
                "type": "text",
                "lines": [
                    "After 10 minutes",
                    f"Trees      : {sum(c == '|' for row in grid for c in row)}",
                    f"Lumberyards: {sum(c == '#' for row in grid for c in row)}",
                    f"Part 1     : {resource(grid)}",
                ],
                "delay": 1200,
            }
