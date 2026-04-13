"""
Day 07 - Recursive Circus
Year: 2017

Part 1: Find the bottom program (root of the tree).
Part 2: Find the incorrect weight and compute the corrected value.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    weights = {}
    children = {}
    all_children = set()

    # Parse input
    for line in lines:
        parts = line.split("->")
        left = parts[0].strip()
        name, w = left.split()[0], int(left.split()[1].strip("()"))
        weights[name] = w

        if len(parts) > 1:
            kids = [c.strip() for c in parts[1].split(",")]
            children[name] = kids
            all_children.update(kids)
        else:
            children[name] = []

    # Part 1: bottom program = parent not in children
    all_parents = set(children.keys())
    part1 = (all_parents - all_children).pop()

    # Part 2: find imbalance
    def total_weight(node):
        """Return (total subtree weight, corrected_weight or None)."""
        child_weights = []
        for c in children[node]:
            tw, fix = total_weight(c)
            if fix is not None:
                return 0, fix  # propagate correction upward
            child_weights.append((c, tw))

        # If no children, just return own weight
        if not child_weights:
            return weights[node], None

        # Check if children are balanced
        counts = {}
        for c, tw in child_weights:
            counts.setdefault(tw, []).append(c)

        if len(counts) == 1:
            # Balanced
            return weights[node] + sum(tw for _, tw in child_weights), None

        # Unbalanced: find the wrong child
        # One weight occurs once, the other occurs multiple times
        wrong_weight = next(w for w, lst in counts.items() if len(lst) == 1)
        right_weight = next(w for w, lst in counts.items() if len(lst) > 1)
        wrong_child = counts[wrong_weight][0]

        # Compute corrected weight
        diff = right_weight - wrong_weight
        corrected = weights[wrong_child] + diff
        return 0, corrected

    _, part2 = total_weight(part1)

    return part1, str(part2)



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
