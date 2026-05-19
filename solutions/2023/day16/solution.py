"""
Day 16 - The Floor Will Be Lava
Year: 2023

Trace light beams through a grid of mirrors and splitters,
counting energized tiles.
"""

from collections import deque


# Direction: (dr, dc)
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)


def count_energized(grid, start_r, start_c, start_dir):
    """Trace beams from a starting position and direction, return energized count."""
    rows, cols = len(grid), len(grid[0])
    seen = set()
    queue = deque([(start_r, start_c, start_dir)])

    while queue:
        r, c, d = queue.popleft()
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue
        if (r, c, d) in seen:
            continue
        seen.add((r, c, d))

        ch = grid[r][c]
        dr, dc = d

        if ch == ".":
            next_dirs = [d]
        elif ch == "/":
            next_dirs = [(-dc, -dr)]
        elif ch == "\\":
            next_dirs = [(dc, dr)]
        elif ch == "|":
            if dc == 0:  # vertical beam passes through
                next_dirs = [d]
            else:  # horizontal beam splits
                next_dirs = [UP, DOWN]
        elif ch == "-":
            if dr == 0:  # horizontal beam passes through
                next_dirs = [d]
            else:  # vertical beam splits
                next_dirs = [LEFT, RIGHT]

        for nd in next_dirs:
            queue.append((r + nd[0], c + nd[1], nd))

    return len({(r, c) for r, c, _ in seen})


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    # Part 1: beam enters top-left going right
    part1 = count_energized(grid, 0, 0, RIGHT)

    # Part 2: try all edge entries, find maximum
    best = 0
    for r in range(rows):
        best = max(best, count_energized(grid, r, 0, RIGHT))
        best = max(best, count_energized(grid, r, cols - 1, LEFT))
    for c in range(cols):
        best = max(best, count_energized(grid, 0, c, DOWN))
        best = max(best, count_energized(grid, rows - 1, c, UP))
    part2 = best

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing beam tracing."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    # Trace default beam to show energized tiles
    seen = set()
    queue = deque([(0, 0, RIGHT)])
    while queue:
        r, c, d = queue.popleft()
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue
        if (r, c, d) in seen:
            continue
        seen.add((r, c, d))
        ch = grid[r][c]
        dr, dc = d
        if ch == ".":
            next_dirs = [d]
        elif ch == "/":
            next_dirs = [(-dc, -dr)]
        elif ch == "\\":
            next_dirs = [(dc, dr)]
        elif ch == "|":
            next_dirs = [d] if dc == 0 else [UP, DOWN]
        elif ch == "-":
            next_dirs = [d] if dr == 0 else [LEFT, RIGHT]
        for nd in next_dirs:
            queue.append((r + nd[0], c + nd[1], nd))

    energized = {(r, c) for r, c, _ in seen}
    cells = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if grid[r][c] in r"/\|-":
                row.append("M")
            elif (r, c) in energized:
                row.append("E")
            else:
                row.append(".")
        cells.append(row)

    colors = {"M": "#ffffff", "E": "#ff6600", ".": "#0f0f23"}
    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 400}

    part1, part2 = solve(puzzle_input)
    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (top-left entry)",
            f"  Part 2: {part2} (best entry)",
        ],
        "delay": 500,
    }
