"""
Day 06 - Probably a Fire Hazard
Year: 2015

Apply rectangle turn-on/turn-off/toggle instructions to a 1000x1000 light grid.
Part 1: lights are on/off. Part 2: lights have integer brightness.
"""
import re


def parse(puzzle_input: str):
    for line in puzzle_input.strip().split("\n"):
        nums = list(map(int, re.findall(r"\d+", line)))
        x1, y1, x2, y2 = nums
        if line.startswith("turn on"):
            op = "on"
        elif line.startswith("turn off"):
            op = "off"
        else:
            op = "toggle"
        yield op, x1, y1, x2, y2


def solve(puzzle_input: str) -> tuple[str, str]:
    # Part 1: binary on/off using bytearray (fast slice assignment)
    grid1 = bytearray(1000 * 1000)
    # Part 2: integer brightness
    grid2 = [0] * (1000 * 1000)

    w = 1000
    for op, x1, y1, x2, y2 in parse(puzzle_input):
        span = y2 - y1 + 1
        for x in range(x1, x2 + 1):
            start = x * w + y1
            end   = start + span
            if op == "on":
                grid1[start:end] = b"\x01" * span
                grid2[start:end] = [v + 1 for v in grid2[start:end]]
            elif op == "off":
                grid1[start:end] = b"\x00" * span
                grid2[start:end] = [max(v - 1, 0) for v in grid2[start:end]]
            else:
                grid1[start:end] = bytes(b ^ 1 for b in grid1[start:end])
                grid2[start:end] = [v + 2 for v in grid2[start:end]]

    return str(sum(grid1)), str(sum(grid2))


def visualize(puzzle_input: str):
    """Animate the on/off grid at 100x100 resolution as instructions are applied."""
    instructions = list(parse(puzzle_input))
    grid = bytearray(1000 * 1000)
    w = 1000
    total = len(instructions)
    step = max(1, total // 120)

    for i, (op, x1, y1, x2, y2) in enumerate(instructions):
        span = y2 - y1 + 1
        for x in range(x1, x2 + 1):
            start = x * w + y1
            end   = start + span
            if op == "on":
                grid[start:end] = b"\x01" * span
            elif op == "off":
                grid[start:end] = b"\x00" * span
            else:
                grid[start:end] = bytes(b ^ 1 for b in grid[start:end])

        if i % step != 0 and i != total - 1:
            continue

        # Downsample 1000x1000 → 100x100 by sampling every 10th cell
        cells = [
            ["#" if grid[(row * 10) * w + (col * 10)] else "." for col in range(100)]
            for row in range(100)
        ]

        yield {
            "type": "grid",
            "cells": cells,
            "colors": {"#": "#ffdd00", ".": "#0f0f23"},
            "delay": 60,
        }