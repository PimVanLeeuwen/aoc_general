"""
Day 23 - Coprocessor Conflagration
Year: 2017

Simulate a small assembly program and reverse-engineer its behavior.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    lines = [line.split() for line in puzzle_input.strip().split("\n")]

    def val(x, regs):
        return regs[x] if x.isalpha() else int(x)

    regs = {chr(c): 0 for c in range(ord("a"), ord("h") + 1)}
    ip = 0
    mul_count = 0

    while 0 <= ip < len(lines):
        op, X, *rest = lines[ip]
        Y = rest[0] if rest else None

        if op == "set":
            regs[X] = val(Y, regs)
        elif op == "sub":
            regs[X] -= val(Y, regs)
        elif op == "mul":
            regs[X] *= val(Y, regs)
            mul_count += 1
        elif op == "jnz":
            if val(X, regs) != 0:
                ip += val(Y, regs)
                continue

        ip += 1

    part1 = str(mul_count)

    # Parse the first few instructions to extract b0
    b0 = int(lines[0][2])
    b = b0 * 100 + 100000
    c = b + 17000

    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        r = int(n**0.5)
        for i in range(3, r + 1, 2):
            if n % i == 0:
                return False
        return True

    h = 0
    for x in range(b, c + 1, 17):
        if not is_prime(x):
            h += 1

    part2 = str(h)

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
