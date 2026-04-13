"""
Day 17 - Spinlock
Year: 2017

Simulate a circular buffer insertion algorithm and determine values after specific positions.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    step = int(puzzle_input.strip())

    buffer = [0]
    pos = 0

    for value in range(1, 2018):
        pos = (pos + step) % len(buffer)
        buffer.insert(pos + 1, value)
        pos += 1

    # Value after 2017
    idx_2017 = buffer.index(2017)
    part1 = buffer[idx_2017 + 1]

    pos = 0
    value_after_zero = None
    size = 1  # virtual buffer size

    for value in range(1, 50_000_001):
        pos = (pos + step) % size
        if pos == 0:
            value_after_zero = value
        pos += 1
        size += 1

    part2 = value_after_zero

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
