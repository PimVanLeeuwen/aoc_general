"""
Day 11 - Seating System
Year: 2020

Cellular automaton on a seating layout — adjacent seats (Part 1) vs
line-of-sight seats (Part 2) with different tolerance thresholds.
"""

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def step_adjacent(grid, h, w):
    """One step using immediate neighbors (Part 1 rules)."""
    new = [row[:] for row in grid]
    changed = False
    for y in range(h):
        for x in range(w):
            if grid[y][x] == ".":
                continue
            occupied = 0
            for dy, dx in DIRS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < len(grid[ny]) and grid[ny][nx] == "#":
                    occupied += 1
            if grid[y][x] == "L" and occupied == 0:
                new[y][x] = "#"
                changed = True
            elif grid[y][x] == "#" and occupied >= 4:
                new[y][x] = "L"
                changed = True
    return new, changed


def step_visible(grid, h, w):
    """One step using line-of-sight neighbors (Part 2 rules)."""
    new = [row[:] for row in grid]
    changed = False
    for y in range(h):
        for x in range(w):
            if grid[y][x] == ".":
                continue
            occupied = 0
            for dy, dx in DIRS:
                ny, nx = y + dy, x + dx
                while 0 <= ny < h and 0 <= nx < len(grid[ny]):
                    if grid[ny][nx] == "#":
                        occupied += 1
                        break
                    if grid[ny][nx] == "L":
                        break
                    ny += dy
                    nx += dx
            if grid[y][x] == "L" and occupied == 0:
                new[y][x] = "#"
                changed = True
            elif grid[y][x] == "#" and occupied >= 5:
                new[y][x] = "L"
                changed = True
    return new, changed


def count_occupied(grid):
    """Count occupied seats in the grid."""
    return sum(row.count("#") for row in grid)


def simulate(grid, step_fn):
    """Run simulation until stable, return occupied count."""
    h, w = len(grid), len(grid[0])
    while True:
        grid, changed = step_fn(grid, h, w)
        if not changed:
            return count_occupied(grid)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [list(line) for line in puzzle_input.strip().split("\n") if line.strip()]

    part1 = simulate([row[:] for row in grid], step_adjacent)
    part2 = simulate([row[:] for row in grid], step_visible)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the seating simulation."""
    grid = [list(line) for line in puzzle_input.strip().split("\n")]
    h, w = len(grid), len(grid[0])
    seats = sum(row.count("L") for row in grid)

    yield {
        "type": "text",
        "lines": [
            "  Seating System",
            "",
            f"  Layout: {w}x{h}",
            f"  Seats: {seats}",
            f"  Floor tiles: {h * w - seats}",
        ],
        "delay": 600,
    }

    # Animate Part 1
    current = [row[:] for row in grid]
    steps = 0
    while True:
        current, changed = step_adjacent(current, h, w)
        steps += 1
        if not changed:
            break

    part1 = count_occupied(current)

    # Show final state (downsampled if large)
    display = current
    if h > 50 or w > 100:
        display = current[:50]
    cells = [["#" if c == "#" else "." if c == "." else "L" for c in row] for row in display]

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            ".": "#0f0f23",
            "L": "#333355",
            "#": "#ffff00",
        },
        "delay": 600,
    }

    # Run Part 2
    current2 = [row[:] for row in grid]
    steps2 = 0
    while True:
        current2, changed = step_visible(current2, h, w)
        steps2 += 1
        if not changed:
            break
    part2 = count_occupied(current2)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} occupied ({steps} rounds, adjacent)",
            f"  Part 2: {part2} occupied ({steps2} rounds, line-of-sight)",
        ],
        "delay": 500,
    }
