"""
Day 3 - Toboggan Trajectory
Year: 2020

Count trees hit while sliding down a repeating grid at various slopes.
"""

from math import prod


def count_trees(grid, dx, dy):
    """Count trees hit on slope (dx, dy) through the repeating grid."""
    x, trees = 0, 0
    width = len(grid[0])
    for y in range(dy, len(grid), dy):
        x += dx
        if grid[y][x % width] == "#":
            trees += 1
    return trees


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = [count_trees(grid, dx, dy) for dx, dy in slopes]

    part1 = counts[1]  # slope (3, 1)
    part2 = prod(counts)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the toboggan path."""
    grid = puzzle_input.strip().split("\n")
    height = len(grid)
    width = len(grid[0])

    # Show the grid with the main slope (3,1) path highlighted
    cells = []
    x = 0
    path = set()
    hits = set()
    for y in range(height):
        if y > 0:
            x += 3
        pos = x % width
        path.add((pos, y))
        if grid[y][pos] == "#":
            hits.add((pos, y))

    for y in range(min(height, 40)):
        row = []
        for xi in range(width):
            if (xi, y) in hits:
                row.append("X")
            elif (xi, y) in path:
                row.append("O")
            elif grid[y][xi] == "#":
                row.append("#")
            else:
                row.append(".")
        cells.append(row)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            ".": "#0f0f23",
            "#": "#00aa00",
            "O": "#4488ff",
            "X": "#ff4444",
        },
        "delay": 800,
    }

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = [count_trees(grid, dx, dy) for dx, dy in slopes]

    lines = ["  Toboggan Trajectory", "", f"  Grid: {width}x{height} (repeating)", ""]
    for (dx, dy), c in zip(slopes, counts):
        marker = " <--" if (dx, dy) == (3, 1) else ""
        lines.append(f"  Slope ({dx},{dy}): {c} trees{marker}")

    lines += [
        "",
        "  ===================================",
        f"  Part 1: {counts[1]}",
        f"  Part 2: {prod(counts)}",
    ]

    yield {
        "type": "text",
        "lines": lines,
        "delay": 500,
    }
