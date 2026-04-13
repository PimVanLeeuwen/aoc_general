"""
Day 25 - The Halting Problem
Year: 2017

Simulate a Turing machine from a textual blueprint and compute its checksum.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = [line.strip() for line in puzzle_input.strip().split("\n") if line.strip()]

    begin_state = lines[0].split()[-1].strip(".")
    steps = int(lines[1].split()[-2])

    i = 2
    rules = {}

    while i < len(lines):
        if not lines[i].startswith("In state"):
            i += 1
            continue

        state = lines[i].split()[-1].strip(":")
        i += 1

        state_rules = {}

        for _ in range(2):  # for value 0 and 1
            # If the current value is X:
            value = int(lines[i].split()[-1].strip(":"))
            i += 1
            # - Write the value Y.
            write_val = int(lines[i].split()[-1].strip("."))
            i += 1
            # - Move one slot to the left/right.
            move_dir = lines[i].split()[-1].strip(".")
            move = -1 if move_dir == "left" else 1
            i += 1
            # - Continue with state Z.
            next_state = lines[i].split()[-1].strip(".")
            i += 1

            state_rules[value] = (write_val, move, next_state)

        rules[state] = state_rules

    # Simulate Turing machine
    tape = {}
    cursor = 0
    state = begin_state

    for _ in range(steps):
        cur_val = tape.get(cursor, 0)
        write_val, move, next_state = rules[state][cur_val]
        tape[cursor] = write_val
        cursor += move
        state = next_state

    checksum = sum(tape.values())
    part1 = str(checksum)

    # No official Part 2 for this day
    part2 = ""

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
