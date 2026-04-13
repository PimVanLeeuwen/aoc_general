"""
Day 06 - Memory Reallocation
Year: 2017

Simulate a memory reallocation routine until a configuration repeats,
then measure both the number of cycles to first repeat and the loop size.
"""


def redistribute(banks: list[int]) -> None:
    """Perform one redistribution cycle in-place."""
    n = len(banks)
    idx = max(range(n), key=lambda i: banks[i])
    blocks = banks[idx]
    banks[idx] = 0

    i = (idx + 1) % n
    while blocks > 0:
        banks[i] += 1
        blocks -= 1
        i = (i + 1) % n


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    banks = [int(x) for x in puzzle_input.strip().split()]
    seen: dict[tuple[int, ...], int] = {}

    cycles = 0
    while True:
        state = tuple(banks)
        if state in seen:
            first_seen_at = seen[state]
            part1 = cycles
            part2 = cycles - first_seen_at
            return str(part1), str(part2)

        seen[state] = cycles
        redistribute(banks)
        cycles += 1



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
