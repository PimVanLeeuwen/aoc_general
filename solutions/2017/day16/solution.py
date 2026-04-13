"""
Day 16 - Permutation Promenade
Year: 2017

Sixteen programs, labeled a through p, perform a dance consisting of three types of moves.
Each move transforms the ordering of the programs.
The challenge is to apply the full sequence once (Part 1) and then one billion times (Part 2).
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    moves = puzzle_input.strip().split(",")

    def dance(order):
        arr = list(order)
        for m in moves:
            if m[0] == "s":  # spin
                X = int(m[1:])
                arr = arr[-X:] + arr[:-X]
            elif m[0] == "x":  # exchange
                A, B = map(int, m[1:].split("/"))
                arr[A], arr[B] = arr[B], arr[A]
            elif m[0] == "p":  # partner
                A, B = m[1:].split("/")
                ia = arr.index(A)
                ib = arr.index(B)
                arr[ia], arr[ib] = arr[ib], arr[ia]
        return "".join(arr)

    start = "abcdefghijklmnop"
    part1 = dance(start)

    seen = []
    current = start

    for i in range(1_000_000_000):
        if current in seen:
            # cycle found
            cycle_start = seen.index(current)
            cycle_len = len(seen) - cycle_start
            remaining = (1_000_000_000 - cycle_start) % cycle_len
            part2 = seen[cycle_start + remaining]
            break

        seen.append(current)
        current = dance(current)
    else:
        # no cycle (theoretically impossible here)
        part2 = current

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
