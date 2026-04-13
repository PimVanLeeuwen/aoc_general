"""
Day 19 - A Series of Tubes
Year: 2017

Traverse an ASCII routing diagram, collecting letters and counting steps.
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    grid = puzzle_input.split("\n")

    # Find starting column (the only '|' in the top row)
    row = 0
    col = grid[0].index("|")

    # Directions: down, up, right, left
    directions = {
        "down":  (1, 0),
        "up":    (-1, 0),
        "right": (0, 1),
        "left":  (0, -1),
    }

    direction = "down"
    letters = []
    steps = 0

    def get(r, c):
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
            return grid[r][c]
        return " "  # outside grid

    while True:
        dr, dc = directions[direction]
        row += dr
        col += dc
        steps += 1

        ch = get(row, col)
        if ch == " ":
            break  # end of path

        if ch.isalpha():
            letters.append(ch)

        if ch == "+":
            # Need to turn: try perpendicular directions
            if direction in ("up", "down"):
                # Try left or right
                if get(row, col - 1) not in (" ",):
                    direction = "left"
                else:
                    direction = "right"
            else:
                # Try up or down
                if get(row - 1, col) not in (" ",):
                    direction = "up"
                else:
                    direction = "down"

    part1 = "".join(letters)
    part2 = str(steps)

    return part1, part2



# ── Optional visualizer ────────────────────────────────────────────────────────
# Uncomment and implement to enable the Visualization tab in the portfolio.

def visualize(puzzle_input: str):
    """Yield visualization frames showing the packet walking the tube network."""
    grid = puzzle_input.split("\n")

    # Find starting column (the only '|' in the top row)
    row = 0
    col = grid[0].index("|")

    # Directions: down, up, right, left
    directions = {
        "down":  (1, 0),
        "up":    (-1, 0),
        "right": (0, 1),
        "left":  (0, -1),
    }

    direction = "down"
    letters = []
    steps = 0

    def get(r, c):
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
            return grid[r][c]
        return " "

    # Helper to build a colored grid frame
    def frame():
        cells = []
        for r, line in enumerate(grid):
            row_cells = []
            for c, ch in enumerate(line):
                if r == row and c == col:
                    row_cells.append("@")  # packet position
                else:
                    row_cells.append(ch)
            cells.append(row_cells)

        return {
            "type": "grid",
            "cells": cells,
            "colors": {
                "|": "#00aaff",
                "-": "#00aaff",
                "+": "#ffaa00",
                "@": "#ff00ff",   # packet
                " ": "#000000",
            },
            "delay": 40,
        }

    # Emit initial frame
    yield frame()

    # Walk the maze
    while True:
        dr, dc = directions[direction]
        row += dr
        col += dc
        steps += 1

        ch = get(row, col)
        if ch == " ":
            break

        if ch.isalpha():
            letters.append(ch)

        if ch == "+":
            # Need to turn: try perpendicular directions
            if direction in ("up", "down"):
                if get(row, col - 1) not in (" ",):
                    direction = "left"
                else:
                    direction = "right"
            else:
                if get(row - 1, col) not in (" ",):
                    direction = "up"
                else:
                    direction = "down"

        # Emit frame every step (limit to ~500 frames)
        if steps % 2 == 0:  # skip every other frame to reduce count
            yield frame()

    # Final text summary
    yield {
        "type": "text",
        "lines": [
            "Traversal complete.",
            f"Letters collected: {''.join(letters)}",
            f"Total steps: {steps}",
        ],
        "delay": 500,
    }

