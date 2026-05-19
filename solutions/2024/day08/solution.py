"""
Day 8 - Resonant Collinearity
Year: 2024

Find antinode positions created by pairs of same-frequency
antennas on a grid.
"""

from collections import defaultdict
from itertools import combinations


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = puzzle_input.strip().split("\n")
    rows = len(grid)
    cols = len(grid[0])

    # Group antenna positions by frequency
    antennas = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != ".":
                antennas[grid[r][c]].append((r, c))

    antinodes_p1 = set()
    antinodes_p2 = set()

    for freq, positions in antennas.items():
        for a, b in combinations(positions, 2):
            dr = b[0] - a[0]
            dc = b[1] - a[1]

            # Part 1: antinodes at exactly 2x distance from one antenna
            p1 = (a[0] - dr, a[1] - dc)
            p2 = (b[0] + dr, b[1] + dc)
            if 0 <= p1[0] < rows and 0 <= p1[1] < cols:
                antinodes_p1.add(p1)
            if 0 <= p2[0] < rows and 0 <= p2[1] < cols:
                antinodes_p1.add(p2)

            # Part 2: all grid-aligned positions along the line
            for direction in [1, -1]:
                r, c = a
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes_p2.add((r, c))
                    r += direction * dr
                    c += direction * dc

    return str(len(antinodes_p1)), str(len(antinodes_p2))


def visualize(puzzle_input: str):
    grid = puzzle_input.strip().split("\n")
    rows = len(grid)
    cols = len(grid[0])

    antennas = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != ".":
                antennas[grid[r][c]].append((r, c))

    display_rows = min(25, rows)
    display_cols = min(50, cols)
    cells = []
    colors = {"#": "#ff0000", ".": "#333333"}
    # Add colors for different antenna frequencies
    for ch in antennas:
        colors[ch] = "#00ff41"

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
            "  Resonant Collinearity",
            "  ===================================",
            "",
            f"  Grid: {rows} x {cols}",
            f"  Frequencies: {len(antennas)}",
            f"  Part 1: {part1} (single antinodes)",
            f"  Part 2: {part2} (resonant harmonics)",
        ],
        "delay": 500,
    }
