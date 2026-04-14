"""
Day 02 - Bathroom Security
Year: 2016

Follow movement instructions on a keypad to determine the bathroom code.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    keypad1 = {
        (0, 0): "1", (1, 0): "2", (2, 0): "3",
        (0, 1): "4", (1, 1): "5", (2, 1): "6",
        (0, 2): "7", (1, 2): "8", (2, 2): "9",
    }

    x, y = 1, 1  # starting on '5'
    part1 = ""

    moves = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    for line in lines:
        for c in line:
            dx, dy = moves[c]
            nx, ny = x + dx, y + dy
            if (nx, ny) in keypad1:
                x, y = nx, ny
        part1 += keypad1[(x, y)]

    keypad2 = {
                 (2, 0): "1",
        (1, 1): "2", (2, 1): "3", (3, 1): "4",
        (0, 2): "5", (1, 2): "6", (2, 2): "7", (3, 2): "8", (4, 2): "9",
        (1, 3): "A", (2, 3): "B", (3, 3): "C",
                 (2, 4): "D",
    }

    x, y = 0, 2  # '5' in the diamond layout
    part2 = ""

    for line in lines:
        for c in line:
            dx, dy = moves[c]
            nx, ny = x + dx, y + dy
            if (nx, ny) in keypad2:
                x, y = nx, ny
        part2 += keypad2[(x, y)]

    return part1, part2



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
