"""
Day 21 - Fractal Art
Year: 2017

Enhance a pixel grid using transformation rules with rotation and flipping.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    # Parse rules
    rules = {}
    for line in puzzle_input.strip().split("\n"):
        left, right = line.split(" => ")
        rules[left] = right

    # Convert pattern string to tuple of strings
    def parse(pattern):
        return tuple(pattern.split("/"))

    # Rotate a square pattern 90 degrees clockwise
    def rotate(p):
        n = len(p)
        return tuple("".join(p[n - j - 1][i] for j in range(n)) for i in range(n))

    # Flip horizontally
    def flip(p):
        return tuple(row[::-1] for row in p)

    # Generate all 8 symmetries of a pattern
    def variants(p):
        out = []
        cur = p
        for _ in range(4):
            out.append(cur)
            out.append(flip(cur))
            cur = rotate(cur)
        return out

    # Precompute rule lookup for all variants
    rulemap = {}
    for left, right in rules.items():
        p = parse(left)
        out = parse(right)
        for v in variants(p):
            rulemap[v] = out

    # Enhance one iteration
    def enhance(grid):
        n = len(grid)
        if n % 2 == 0:
            size = 2
        else:
            size = 3

        blocks = []
        for r in range(0, n, size):
            row_blocks = []
            for c in range(0, n, size):
                block = tuple(grid[r+i][c:c+size] for i in range(size))
                row_blocks.append(rulemap[block])
            blocks.append(row_blocks)

        # Reassemble
        new_block_size = len(blocks[0][0])
        new_size = (n // size) * new_block_size
        new_grid = []
        for br in range(len(blocks)):
            for i in range(new_block_size):
                row = "".join(blocks[br][bc][i] for bc in range(len(blocks)))
                new_grid.append(row)
        return new_grid

    # Initial grid
    grid = [".#.", "..#", "###"]

    # Part 1: 5 iterations
    g = grid[:]
    for _ in range(5):
        g = enhance(g)
    part1 = sum(row.count("#") for row in g)

    # Part 2: 18 iterations
    g = grid[:]
    for _ in range(18):
        g = enhance(g)
    part2 = sum(row.count("#") for row in g)

    return str(part1), str(part2)



# ── Optional visualizer ────────────────────────────────────────────────────────
# Uncomment and implement to enable the Visualization tab in the portfolio.
#
# def visualize(puzzle_input: str):
#     """Yield visualization frames (up to ~500 recommended)."""
#     lines = puzzle_input.strip().split("\n")
#
#     # Grid frame – renders as a pixel canvas:
#     yield {
#         "type": "grid",
#         "cells": [list(row) for row in lines],
#         "colors": {"#": "#00ff41", ".": "#0f0f23"},   # cell → hex color
#         "delay": 100,   # ms before advancing to next frame
#     }
#
#     # Text frame – renders as monospace text:
#     yield {
#         "type": "text",
#         "lines": ["Step 1", "Value: 42"],
#         "delay": 300,
#     }
