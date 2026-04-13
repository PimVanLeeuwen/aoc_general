"""
Day 13 - Packet Scanners
Year: 2017

Part 1: Compute severity when leaving immediately.
Part 2: Find the smallest delay that avoids all scanners.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    layers = {}
    for line in puzzle_input.strip().split("\n"):
        depth, rng = line.split(":")
        layers[int(depth.strip())] = int(rng.strip())

    part1 = 0
    for depth, rng in layers.items():
        period = 2 * (rng - 1)
        if depth % period == 0:
            part1 += depth * rng

    part2 = 0
    while True:
        caught = False
        for depth, rng in layers.items():
            period = 2 * (rng - 1)
            if (depth + part2) % period == 0:
                caught = True
                break
        if not caught:
            break
        part2 += 1

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
