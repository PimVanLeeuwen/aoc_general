"""
Day 18 - Like a GIF For Your Yard
Year: 2015

Conway's Game of Life on a 100x100 grid of lights.
"""


def parse(puzzle_input):
    return {(r, c)
            for r, line in enumerate(puzzle_input.strip().split("\n"))
            for c, ch in enumerate(line) if ch == "#"}


def grid_size(puzzle_input):
    lines = puzzle_input.strip().split("\n")
    return len(lines), len(lines[0])


def step(on, rows, cols, corners_stuck=False):
    candidates = set()
    for r, c in on:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    candidates.add((nr, nc))

    new_on = set()
    for r, c in candidates:
        neighbors = sum(
            (r + dr, c + dc) in on
            for dr in (-1, 0, 1) for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0)
        )
        if (r, c) in on:
            if neighbors in (2, 3):
                new_on.add((r, c))
        else:
            if neighbors == 3:
                new_on.add((r, c))

    if corners_stuck:
        for corner in ((0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)):
            new_on.add(corner)

    return new_on


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rows, cols = grid_size(puzzle_input)
    initial = parse(puzzle_input)

    # Part 1: standard Game of Life
    on = set(initial)
    for _ in range(100):
        on = step(on, rows, cols)
    part1 = len(on)

    # Part 2: four corners always on
    on = set(initial)
    for corner in ((0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)):
        on.add(corner)
    for _ in range(100):
        on = step(on, rows, cols, corners_stuck=True)
    part2 = len(on)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield grid frames showing the Game of Life animation."""
    rows, cols = grid_size(puzzle_input)
    on = parse(puzzle_input)

    # Show Part 1 animation, sampling every few steps
    sample_step = max(1, 100 // 50)
    for i in range(101):
        if i % sample_step == 0 or i == 100:
            grid = [["#" if (r, c) in on else "." for c in range(cols)] for r in range(rows)]
            yield {
                "type": "grid",
                "cells": grid,
                "colors": {"#": "#00ff41", ".": "#0f0f23"},
                "delay": 200 if i == 100 else 100,
            }
        if i < 100:
            on = step(on, rows, cols)
