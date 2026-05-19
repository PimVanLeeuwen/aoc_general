"""
Day 6 - Guard Gallivant
Year: 2024

Simulate a guard walking a grid, turning right on obstacles.
Part 2: find positions where adding an obstacle creates a loop.
"""


DIRECTIONS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
TURN_RIGHT = {"^": ">", ">": "v", "v": "<", "<": "^"}


def find_guard(grid):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in DIRECTIONS:
                return r, c, ch
    return None


def walk(grid, start_r, start_c, start_dir, extra_obstacle=None):
    """Simulate the guard. Returns (visited_positions, looped)."""
    rows, cols = len(grid), len(grid[0])
    r, c, d = start_r, start_c, start_dir
    visited = set()
    seen_states = set()

    while True:
        state = (r, c, d)
        if state in seen_states:
            return visited, True
        seen_states.add(state)
        visited.add((r, c))

        dr, dc = DIRECTIONS[d]
        nr, nc = r + dr, c + dc

        if not (0 <= nr < rows and 0 <= nc < cols):
            return visited, False

        blocked = grid[nr][nc] == "#" or (extra_obstacle and (nr, nc) == extra_obstacle)
        if blocked:
            d = TURN_RIGHT[d]
        else:
            r, c = nr, nc


def solve(puzzle_input: str) -> tuple[str, str]:
    grid = puzzle_input.strip().split("\n")
    start_r, start_c, start_dir = find_guard(grid)

    # Part 1: count distinct visited positions
    visited, _ = walk(grid, start_r, start_c, start_dir)
    part1 = len(visited)

    # Part 2: try placing an obstacle on each visited cell
    part2 = 0
    for r, c in visited:
        if (r, c) == (start_r, start_c):
            continue
        _, looped = walk(grid, start_r, start_c, start_dir, extra_obstacle=(r, c))
        if looped:
            part2 += 1

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])
    start_r, start_c, start_dir = find_guard(grid)

    visited, _ = walk(grid, start_r, start_c, start_dir)

    # Show the path on a cropped grid
    display_rows = min(30, rows)
    display_cols = min(50, cols)
    cells = []
    colors = {"#": "#666666", "*": "#00ff41", "^": "#ff0000"}

    for r in range(display_rows):
        row = []
        for c in range(display_cols):
            if (r, c) in visited:
                row.append("*")
            elif grid[r][c] == "#":
                row.append("#")
            else:
                row.append(" ")
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 800}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Guard Gallivant",
            "  ===================================",
            "",
            f"  Grid: {rows} x {cols}",
            f"  Part 1: {part1} (visited positions)",
            f"  Part 2: {part2} (loop positions)",
        ],
        "delay": 500,
    }
