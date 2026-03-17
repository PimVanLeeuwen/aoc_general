"""
Day 13 - Mine Cart Madness
Year: 2018

Simulate mine carts moving on a track grid.
Part 1: location of the first collision.
Part 2: location of the last cart standing after all collisions are resolved.
"""

# Cart characters and their (dy, dx) direction vectors
CART_DIR = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

# How curves redirect movement: (dy, dx) -> (dy, dx)
CURVE = {
    "/":  {(-1, 0): (0, 1), (0, 1): (-1, 0), (1, 0): (0, -1), (0, -1): (1, 0)},
    "\\": {(-1, 0): (0, -1), (0, -1): (-1, 0), (1, 0): (0, 1), (0, 1): (1, 0)},
}

# Intersection turn order: left, straight, right (relative to current direction)
# Encoded as index into LEFT_TURN / RIGHT_TURN
def turn_left(dy, dx):
    return -dx, dy

def turn_right(dy, dx):
    return dx, -dy


def parse(puzzle_input: str):
    lines = puzzle_input.splitlines()
    grid = {}
    # carts: dict of (y, x) -> [dy, dx, turn_state]  (turn_state: 0=left,1=str,2=right)
    carts = {}
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch in CART_DIR:
                dy, dx = CART_DIR[ch]
                carts[(y, x)] = [dy, dx, 0]
                # Replace cart with underlying track
                ch = "|" if dx == 0 else "-"
            grid[(y, x)] = ch
    return grid, carts


def tick(grid: dict, carts: dict) -> list[tuple[int, int]]:
    """Move all carts one step in reading order. Returns list of collision positions."""
    collisions = []
    for pos in sorted(carts):
        if pos not in carts:
            continue  # already removed by collision this tick
        dy, dx, turn = carts.pop(pos)
        ny, nx = pos[0] + dy, pos[1] + dx
        cell = grid.get((ny, nx), " ")

        if cell in CURVE:
            dy, dx = CURVE[cell][(dy, dx)]
        elif cell == "+":
            if turn == 0:
                dy, dx = turn_left(dy, dx)
            elif turn == 2:
                dy, dx = turn_right(dy, dx)
            turn = (turn + 1) % 3

        if (ny, nx) in carts:
            collisions.append((nx, ny))
            del carts[(ny, nx)]
        else:
            carts[(ny, nx)] = [dy, dx, turn]

    return collisions


def solve(puzzle_input: str) -> tuple[str, str]:
    grid, carts = parse(puzzle_input)

    first_crash = None
    while len(carts) > 1:
        crashes = tick(grid, carts)
        if first_crash is None and crashes:
            first_crash = crashes[0]

    part1 = f"{first_crash[0]},{first_crash[1]}" if first_crash else ""
    last = next(iter(carts)) if carts else None
    part2 = f"{last[1]},{last[0]}" if last else ""

    return part1, part2


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    grid, carts = parse(puzzle_input)

    COLORS = {
        "-": "#1a3a1a", "|": "#1a3a1a", "/": "#1a3a1a", "\\": "#1a3a1a",
        "+": "#2a5a2a",
        "^": "#00ff41", "v": "#00ff41", "<": "#00ff41", ">": "#00ff41",
        "X": "#ff4444",
        " ": "#0a0a0a",
    }

    lines = puzzle_input.splitlines()
    height = len(lines)
    width = max(len(l) for l in lines)

    def render(g, c, crashed):
        cells = []
        for y in range(height):
            row = []
            for x in range(width):
                ch = g.get((y, x), " ")
                if (y, x) in crashed:
                    ch = "X"
                elif (y, x) in c:
                    dy, dx, _ = c[(y, x)]
                    ch = {(-1,0): "^", (1,0): "v", (0,-1): "<", (0,1): ">"}[(dy, dx)]
                row.append(ch)
            cells.append(row)
        return cells

    crashed_positions = set()
    first_crash = None

    yield {"type": "grid", "cells": render(grid, carts, crashed_positions), "colors": COLORS, "delay": 200}

    tick_num = 0
    while len(carts) > 1:
        crashes = tick(grid, carts)
        tick_num += 1
        for cx, cy in crashes:
            crashed_positions.add((cy, cx))
            if first_crash is None:
                first_crash = (cx, cy)

        yield {"type": "grid", "cells": render(grid, carts, crashed_positions), "colors": COLORS, "delay": 80}

        if first_crash and tick_num == 1 or (crashes and first_crash == crashes[0]):
            yield {
                "type": "text",
                "lines": [f"First collision at tick {tick_num}", f"  → {first_crash[0]},{first_crash[1]}"],
                "delay": 800,
            }

    last = next(iter(carts)) if carts else None
    yield {"type": "grid", "cells": render(grid, carts, crashed_positions), "colors": COLORS, "delay": 500}
    if last:
        yield {
            "type": "text",
            "lines": [
                f"Simulation complete ({tick_num} ticks)",
                "",
                f"First crash : {first_crash[0]},{first_crash[1]}" if first_crash else "No crash",
                f"Last cart   : {last[1]},{last[0]}",
            ],
            "delay": 4000,
        }
