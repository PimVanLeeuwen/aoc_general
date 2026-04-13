"""
Day 09 - Stream Processing
Year: 2017

Part 1: Compute the total score of all groups.
Part 2: Count the number of non-canceled garbage characters.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    stream = puzzle_input.strip()

    depth = 0
    part1 = 0
    part2 = 0

    garbage = False
    skip = False


    for ch in stream:
        if skip:
            skip = False
            continue

        if ch == "!":
            skip = True
            continue

        if garbage:
            if ch == ">":
                garbage = False
            else:
                part2 += 1
            continue

        # Not in garbage
        if ch == "<":
            garbage = True
        elif ch == "{":
            depth += 1
            part1 += depth
        elif ch == "}":
            depth -= 1

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
