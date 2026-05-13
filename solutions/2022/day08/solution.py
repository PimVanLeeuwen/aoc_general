"""
Day 8 - Treetop Tree House
Year: 2022

Determine tree visibility and scenic scores in a height grid.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    rows = len(grid)
    cols = len(grid[0])

    # Part 1: sweep from each edge to mark visible trees
    visible = [[False] * cols for _ in range(rows)]

    for r in range(rows):
        max_left = -1
        max_right = -1
        for c in range(cols):
            if grid[r][c] > max_left:
                max_left = grid[r][c]
                visible[r][c] = True
            if grid[r][cols - 1 - c] > max_right:
                max_right = grid[r][cols - 1 - c]
                visible[r][cols - 1 - c] = True

    for c in range(cols):
        max_top = -1
        max_bottom = -1
        for r in range(rows):
            if grid[r][c] > max_top:
                max_top = grid[r][c]
                visible[r][c] = True
            if grid[rows - 1 - r][c] > max_bottom:
                max_bottom = grid[rows - 1 - r][c]
                visible[rows - 1 - r][c] = True

    part1 = sum(visible[r][c] for r in range(rows) for c in range(cols))

    # Part 2: scenic score for each tree
    best_score = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(rows):
        for c in range(cols):
            score = 1
            for dr, dc in directions:
                dist = 0
                nr, nc = r + dr, c + dc
                while 0 <= nr < rows and 0 <= nc < cols:
                    dist += 1
                    if grid[nr][nc] >= grid[r][c]:
                        break
                    nr += dr
                    nc += dc
                score *= dist
            best_score = max(best_score, score)

    return str(part1), str(best_score)


def visualize(puzzle_input: str):
    """Yield frames showing tree visibility."""
    grid = [[int(c) for c in line] for line in puzzle_input.strip().split("\n")]
    rows = len(grid)
    cols = len(grid[0])

    colors = {}
    for h in range(10):
        green = int(40 + h * 20)
        colors[str(h)] = f"#00{green:02x}00"

    cells = [[str(grid[r][c]) for c in range(cols)] for r in range(rows)]

    yield {
        "type": "grid",
        "cells": cells,
        "colors": colors,
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (visible trees)",
            f"  Part 2: {part2} (best scenic score)",
        ],
        "delay": 500,
    }
