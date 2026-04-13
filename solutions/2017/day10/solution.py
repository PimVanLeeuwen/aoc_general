"""
Day 10 - Knot Hash
Year: 2017

Part 1: Perform one round of the knot-tying algorithm and multiply the first two numbers.
Part 2: Compute the full Knot Hash of the input.
"""

def knot_round(nums, lengths, pos=0, skip=0):
    n = len(nums)
    for length in lengths:
        # Reverse the segment
        idxs = [(pos + i) % n for i in range(length)]
        vals = [nums[i] for i in idxs][::-1]
        for i, v in zip(idxs, vals):
            nums[i] = v

        pos = (pos + length + skip) % n
        skip += 1

    return pos, skip


def dense_hash(sparse):
    out = []
    for i in range(0, 256, 16):
        x = 0
        for v in sparse[i:i+16]:
            x ^= v
        out.append(x)
    return out


def solve(puzzle_input: str) -> tuple[str, str]:
    raw = puzzle_input.strip()

    nums = list(range(256))
    lengths = [int(x) for x in raw.split(",")]
    knot_round(nums, lengths)
    part1 = nums[0] * nums[1]

    nums = list(range(256))
    lengths = [ord(c) for c in raw] + [17, 31, 73, 47, 23]

    pos = skip = 0
    for _ in range(64):
        pos, skip = knot_round(nums, lengths, pos, skip)

    dense = dense_hash(nums)
    part2 = "".join(f"{x:02x}" for x in dense)

    return str(part1), part2



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
