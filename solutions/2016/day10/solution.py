"""
Day 10 - Balance Bots
Year: 2016

Simulate bots passing microchips and determine comparisons and output values.
"""

from collections import defaultdict, deque

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""

    bot_rules = {}
    bots = defaultdict(list)
    outputs = defaultdict(list)

    value_instructions = []

    # Parse input
    for line in puzzle_input.strip().split("\n"):
        parts = line.split()
        if parts[0] == "value":
            # value X goes to bot Y
            value = int(parts[1])
            bot = int(parts[5])
            value_instructions.append((value, bot))
        else:
            # bot A gives low to X and high to Y
            bot = int(parts[1])
            low_type = parts[5]
            low_id = int(parts[6])
            high_type = parts[10]
            high_id = int(parts[11])
            bot_rules[bot] = (low_type, low_id, high_type, high_id)

    # Initialize bots with starting values
    for value, bot in value_instructions:
        bots[bot].append(value)

    # Queue bots that have two chips
    queue = deque([b for b, chips in bots.items() if len(chips) == 2])

    part1 = None

    # Simulation
    while queue:
        bot = queue.popleft()
        chips = bots[bot]

        if len(chips) < 2:
            continue

        low, high = sorted(chips)

        # Check Part 1 condition (example: comparing 17 and 61)
        if low == 17 and high == 61:
            part1 = bot

        low_type, low_id, high_type, high_id = bot_rules[bot]

        # Give low chip
        if low_type == "bot":
            bots[low_id].append(low)
            if len(bots[low_id]) == 2:
                queue.append(low_id)
        else:
            outputs[low_id].append(low)

        # Give high chip
        if high_type == "bot":
            bots[high_id].append(high)
            if len(bots[high_id]) == 2:
                queue.append(high_id)
        else:
            outputs[high_id].append(high)

        # Bot has given away its chips
        bots[bot] = []

    # Part 2: product of outputs 0, 1, 2
    part2 = outputs[0][0] * outputs[1][0] * outputs[2][0]

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
