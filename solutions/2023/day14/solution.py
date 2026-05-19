"""
Day 14 - Parabolic Reflector Dish
Year: 2023

Tilt a grid of rolling rocks ('O') and fixed rocks ('#'),
then find the load after 1 billion spin cycles.
"""


def tilt_north(grid):
    """Tilt the grid so all 'O' rocks roll north."""
    rows, cols = len(grid), len(grid[0])
    for c in range(cols):
        empty = 0  # next available row for a rolling rock
        for r in range(rows):
            if grid[r][c] == "O":
                grid[r][c] = "."
                grid[empty][c] = "O"
                empty += 1
            elif grid[r][c] == "#":
                empty = r + 1


def rotate_cw(grid):
    """Rotate grid 90 degrees clockwise."""
    rows, cols = len(grid), len(grid[0])
    return [[grid[rows - 1 - r][c] for r in range(rows)] for c in range(cols)]


def spin_cycle(grid):
    """One full spin cycle: tilt N, W, S, E."""
    for _ in range(4):
        tilt_north(grid)
        grid = rotate_cw(grid)
    return grid


def compute_load(grid):
    """Total load: each 'O' contributes (rows - row_index)."""
    rows = len(grid)
    return sum(rows - r for r in range(rows) for c in range(len(grid[0])) if grid[r][c] == "O")


def grid_key(grid):
    """Hashable representation of the grid."""
    return tuple(tuple(row) for row in grid)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [list(row) for row in puzzle_input.strip().split("\n")]

    # Part 1: tilt north once
    p1_grid = [row[:] for row in grid]
    tilt_north(p1_grid)
    part1 = compute_load(p1_grid)

    # Part 2: 1 billion spin cycles with cycle detection
    target = 1_000_000_000
    seen = {}
    g = [row[:] for row in grid]
    for step in range(target):
        key = grid_key(g)
        if key in seen:
            cycle_start = seen[key]
            cycle_len = step - cycle_start
            remaining = (target - step) % cycle_len
            for _ in range(remaining):
                g = spin_cycle(g)
            break
        seen[key] = step
        g = spin_cycle(g)

    part2 = compute_load(g)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing rock tilting."""
    grid = [list(row) for row in puzzle_input.strip().split("\n")]

    colors = {"O": "#ffff00", "#": "#666666", ".": "#0f0f23"}

    yield {"type": "grid", "cells": [row[:] for row in grid], "colors": colors, "delay": 300}

    tilt_north(grid)
    yield {"type": "grid", "cells": [row[:] for row in grid], "colors": colors, "delay": 300}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (tilt north)",
            f"  Part 2: {part2} (1B spin cycles)",
        ],
        "delay": 500,
    }
