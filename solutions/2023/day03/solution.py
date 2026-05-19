"""
Day 3 - Gear Ratios
Year: 2023

Find part numbers adjacent to symbols in a schematic,
and gear ratios for '*' symbols adjacent to exactly two numbers.
"""

import re
from collections import defaultdict


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.strip().split("\n")
    rows, cols = len(grid), len(grid[0])

    def is_symbol(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            ch = grid[r][c]
            return ch != "." and not ch.isdigit()
        return False

    # Find all numbers and their positions
    part1 = 0
    gear_numbers = defaultdict(list)

    for r in range(rows):
        for m in re.finditer(r"\d+", grid[r]):
            num = int(m.group())
            start, end = m.start(), m.end()

            # Check all neighbors of this number
            adjacent_symbols = set()
            for c in range(start, end):
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            ch = grid[nr][nc]
                            if ch != "." and not ch.isdigit():
                                adjacent_symbols.add((nr, nc))

            if adjacent_symbols:
                part1 += num

            for sr, sc in adjacent_symbols:
                if grid[sr][sc] == "*":
                    gear_numbers[(sr, sc)].append(num)

    part2 = sum(
        nums[0] * nums[1]
        for nums in gear_numbers.values()
        if len(nums) == 2
    )

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the schematic."""
    grid = puzzle_input.strip().split("\n")

    colors = {}
    for d in "0123456789":
        colors[d] = "#00ff41"
    colors["."] = "#0f0f23"
    colors["*"] = "#ffff00"

    cells = [list(row) for row in grid[:20]]
    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (part number sum)",
            f"  Part 2: {part2} (gear ratio sum)",
        ],
        "delay": 500,
    }
