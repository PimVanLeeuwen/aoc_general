"""
Day 25 - Sea Cucumber
Year: 2021

Simulate east-facing and south-facing sea cucumber herds on a
toroidal grid until no movement occurs.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [list(line) for line in puzzle_input.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])

    step = 0
    while True:
        moved = False

        # Move east-facing cucumbers
        to_move = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == ">" and grid[r][(c + 1) % cols] == ".":
                    to_move.append((r, c))
        for r, c in to_move:
            grid[r][(c + 1) % cols] = ">"
            grid[r][c] = "."
            moved = True

        # Move south-facing cucumbers
        to_move = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "v" and grid[(r + 1) % rows][c] == ".":
                    to_move.append((r, c))
        for r, c in to_move:
            grid[(r + 1) % rows][c] = "v"
            grid[r][c] = "."
            moved = True

        step += 1
        if not moved:
            break

    return str(step), "0"


def visualize(puzzle_input: str):
    """Yield frames showing sea cucumber movement."""
    grid = [list(line) for line in puzzle_input.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])

    colors = {
        ">": "#00ff41",
        "v": "#ffff00",
        ".": "#0f0f23",
    }

    # Show initial state
    yield {
        "type": "grid",
        "cells": [row[:] for row in grid],
        "colors": colors,
        "delay": 400,
    }

    step = 0
    while True:
        moved = False

        to_move = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == ">" and grid[r][(c + 1) % cols] == ".":
                    to_move.append((r, c))
        for r, c in to_move:
            grid[r][(c + 1) % cols] = ">"
            grid[r][c] = "."
            moved = True

        to_move = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "v" and grid[(r + 1) % rows][c] == ".":
                    to_move.append((r, c))
        for r, c in to_move:
            grid[(r + 1) % rows][c] = "v"
            grid[r][c] = "."
            moved = True

        step += 1

        if step <= 10 or step % 20 == 0 or not moved:
            yield {
                "type": "grid",
                "cells": [row[:] for row in grid],
                "colors": colors,
                "delay": 200 if step <= 10 else 100,
            }

        if not moved:
            break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {step} (first step with no movement)",
            f"  Part 2: (free star)",
        ],
        "delay": 500,
    }
