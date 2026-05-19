"""
Day 10 - Hoof It
Year: 2024

Find hiking trails on a topographic map: paths from height 0
to height 9 that increase by exactly 1 at each step.
"""

from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = []
    for line in puzzle_input.strip().split("\n"):
        grid.append([int(c) for c in line])

    rows = len(grid)
    cols = len(grid[0])

    part1 = 0
    part2 = 0

    for sr in range(rows):
        for sc in range(cols):
            if grid[sr][sc] != 0:
                continue

            # BFS from each trailhead (height 0)
            queue = deque([(sr, sc)])
            reachable_nines = set()
            trail_count = 0

            while queue:
                r, c = queue.popleft()
                if grid[r][c] == 9:
                    reachable_nines.add((r, c))
                    trail_count += 1
                    continue

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == grid[r][c] + 1:
                            queue.append((nr, nc))

            part1 += len(reachable_nines)
            part2 += trail_count

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid = []
    for line in puzzle_input.strip().split("\n"):
        grid.append([int(c) for c in line])

    rows = len(grid)
    cols = len(grid[0])

    trailheads = sum(1 for r in range(rows) for c in range(cols) if grid[r][c] == 0)

    display_rows = min(20, rows)
    display_cols = min(40, cols)
    cells = []
    colors = {
        "0": "#ff0000", "9": "#00ff41",
        "1": "#ff3300", "2": "#ff6600", "3": "#ff9900",
        "4": "#ffcc00", "5": "#ccff00", "6": "#66ff00",
        "7": "#00ff66", "8": "#00ffaa",
    }

    for r in range(display_rows):
        row = []
        for c in range(display_cols):
            row.append(str(grid[r][c]))
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 800}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Hoof It",
            "  ===================================",
            "",
            f"  Grid: {rows} x {cols}",
            f"  Trailheads: {trailheads}",
            f"  Part 1: {part1} (reachable peaks)",
            f"  Part 2: {part2} (distinct trails)",
        ],
        "delay": 500,
    }
