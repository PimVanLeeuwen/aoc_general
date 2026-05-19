"""
Day 11 - Cosmic Expansion
Year: 2023

Sum shortest paths between galaxies in an expanding universe.
Empty rows and columns expand by a factor.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    # Find all galaxies
    galaxies = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                galaxies.append((r, c))

    # Identify empty rows and columns
    galaxy_rows = {r for r, c in galaxies}
    galaxy_cols = {c for r, c in galaxies}
    empty_rows = [r for r in range(rows) if r not in galaxy_rows]
    empty_cols = [c for c in range(cols) if c not in galaxy_cols]

    def total_distance(expansion):
        """Sum Manhattan distances with expanded empty rows/cols."""
        total = 0
        for i in range(len(galaxies)):
            r1, c1 = galaxies[i]
            for j in range(i + 1, len(galaxies)):
                r2, c2 = galaxies[j]
                lo_r, hi_r = min(r1, r2), max(r1, r2)
                lo_c, hi_c = min(c1, c2), max(c1, c2)
                dist = hi_r - lo_r + hi_c - lo_c
                # Each empty row/col in range adds (expansion - 1) extra
                for er in empty_rows:
                    if lo_r < er < hi_r:
                        dist += expansion - 1
                for ec in empty_cols:
                    if lo_c < ec < hi_c:
                        dist += expansion - 1
                total += dist
        return total

    part1 = total_distance(2)
    part2 = total_distance(1_000_000)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing cosmic expansion."""
    grid = puzzle_input.strip().split("\n")
    galaxies = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                galaxies.append((r, c))

    colors = {"#": "#ffff00", ".": "#0f0f23"}
    yield {
        "type": "grid",
        "cells": [list(row) for row in grid],
        "colors": colors,
        "delay": 400,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Galaxies: {len(galaxies)}",
            f"  Part 1: {part1} (expansion=2)",
            f"  Part 2: {part2} (expansion=1M)",
        ],
        "delay": 500,
    }
