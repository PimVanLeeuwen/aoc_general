"""
Day 08 - I Heard You Like Registers
Year: 2017

Simulate a set of conditional register modifications.
Part 1: Largest value in any register after all instructions.
Part 2: Largest value ever held during the process.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")
    regs = {}
    highest_ever = 0

    def get(r):
        return regs.get(r, 0)

    ops = {
        "inc": lambda a, b: a + b,
        "dec": lambda a, b: a - b
    }

    cond_ops = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        ">":  lambda a, b: a > b,
        "<":  lambda a, b: a < b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b
    }

    for line in lines:
        reg, op, amt, _, c_reg, c_op, c_val = line.split()
        amt = int(amt)
        c_val = int(c_val)

        # Evaluate condition
        if cond_ops[c_op](get(c_reg), c_val):
            regs[reg] = ops[op](get(reg), amt)
            highest_ever = max(highest_ever, regs[reg])

    part1 = max(regs.values()) if regs else 0
    part2 = highest_ever

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
