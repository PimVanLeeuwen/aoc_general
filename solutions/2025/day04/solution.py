"""
Day 4 - Rolling Boulders
Year: 2025

Cellular automaton on a grid: boulders (@) with fewer than 4
neighbours are removed. Part 1 counts initial removals,
part 2 iterates until stable.
"""


DIRS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    return sum(
        1 for dr, dc in DIRS_8
        if 0 <= r + dr < rows and 0 <= c + dc < cols and grid[r + dr][c + dc] == "@"
    )


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = [list(line) for line in puzzle_input.split("\n") if line]
    rows, cols = len(grid), len(grid[0])

    # Part 1: count boulders with fewer than 4 neighbours (single pass)
    part1 = sum(
        1 for r in range(rows) for c in range(cols)
        if grid[r][c] == "@" and count_neighbors(grid, r, c) < 4
    )

    # Part 2: iteratively remove unstable boulders until no changes
    part2 = 0
    while True:
        to_remove = [
            (r, c) for r in range(rows) for c in range(cols)
            if grid[r][c] == "@" and count_neighbors(grid, r, c) < 4
        ]
        if not to_remove:
            break
        for r, c in to_remove:
            grid[r][c] = "."
            part2 += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid = [list(line) for line in puzzle_input.split("\n") if line]
    rows, cols = len(grid), len(grid[0])
    boulders = sum(1 for r in range(rows) for c in range(cols) if grid[r][c] == "@")

    display_rows = min(25, rows)
    display_cols = min(50, cols)
    cells = []
    colors = {"@": "#ffaa00", ".": "#1a1a1a"}

    for r in range(display_rows):
        row = []
        for c in range(display_cols):
            row.append(grid[r][c])
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 800}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Rolling Boulders",
            "  ===================================",
            "",
            f"  Grid: {rows} x {cols}, Boulders: {boulders}",
            f"  Part 1: {part1} (initial unstable)",
            f"  Part 2: {part2} (total removed)",
        ],
        "delay": 500,
    }
