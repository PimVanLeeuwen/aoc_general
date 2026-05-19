"""
Day 4 - Ceres Search
Year: 2024

Word search puzzle: find all "XMAS" in 8 directions (part 1)
and all X-shaped "MAS" crosses (part 2).
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = puzzle_input.strip().split("\n")
    rows = len(grid)
    cols = len(grid[0])

    # Part 1: count "XMAS" in all 8 directions
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]
    target = "XMAS"
    part1 = 0

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] != "X":
                continue
            for dy, dx in directions:
                if 0 <= y + 3 * dy < rows and 0 <= x + 3 * dx < cols:
                    word = "".join(grid[y + i * dy][x + i * dx] for i in range(4))
                    if word == target:
                        part1 += 1

    # Part 2: count X-MAS patterns (two diagonal "MAS" crossing at 'A')
    part2 = 0
    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            if grid[y][x] != "A":
                continue
            diag1 = grid[y - 1][x - 1] + grid[y + 1][x + 1]
            diag2 = grid[y - 1][x + 1] + grid[y + 1][x - 1]
            if diag1 in ("MS", "SM") and diag2 in ("MS", "SM"):
                part2 += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid = puzzle_input.strip().split("\n")
    rows = len(grid)
    cols = len(grid[0])

    # Show a small portion of the grid
    display_rows = min(20, rows)
    display_cols = min(40, cols)
    cells = []
    colors = {"X": "#ff0000", "M": "#ffaa00", "A": "#00ff41", "S": "#00aaff"}
    for y in range(display_rows):
        row = []
        for x in range(display_cols):
            row.append(grid[y][x])
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 800}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Ceres Search",
            "  ===================================",
            "",
            f"  Grid size: {rows} x {cols}",
            f"  Part 1: {part1} (XMAS occurrences)",
            f"  Part 2: {part2} (X-MAS crosses)",
        ],
        "delay": 500,
    }
