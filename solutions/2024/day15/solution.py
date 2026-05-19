"""
Day 15 - Warehouse Woes
Year: 2024

Sokoban-like puzzle: push boxes around a warehouse.
Part 2 uses double-width boxes that need careful vertical pushing.
"""


DIRS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def parse_input(text):
    parts = text.split("\n\n")
    grid = [list(line) for line in parts[0].split("\n")]
    moves = parts[1].replace("\n", "")
    return grid, moves


def find_robot(grid):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "@":
                return r, c
    return None


def widen_grid(grid):
    """Create the double-width version of the grid for part 2."""
    wide = []
    for row in grid:
        new_row = []
        for ch in row:
            if ch == "#":
                new_row.extend(["#", "#"])
            elif ch == "O":
                new_row.extend(["[", "]"])
            elif ch == "@":
                new_row.extend(["@", "."])
            else:
                new_row.extend([".", "."])
        wide.append(new_row)
    return wide


def push_horizontal(grid, r, c, dc):
    """Push boxes horizontally. Returns new robot column or original if blocked."""
    # Find the end of the chain of boxes
    nc = c + dc
    while grid[r][nc] in ("O", "[", "]"):
        nc += dc

    if grid[r][nc] == "#":
        return c  # blocked

    # Shift everything from nc back to c+dc
    while nc != c:
        grid[r][nc] = grid[r][nc - dc]
        nc -= dc
    grid[r][c] = "."
    return c + dc


def push_vertical(grid, r, c, dr):
    """Push boxes vertically, handling wide boxes in part 2."""
    # Collect layers of cells that need to move
    layers = [{(r, c)}]

    while True:
        next_layer = set()
        all_empty = True

        for pr, pc in layers[-1]:
            nr = pr + dr
            ch = grid[nr][pc]
            if ch == "#":
                return r, c  # blocked
            if ch != ".":
                all_empty = False
                next_layer.add((nr, pc))
                if ch == "[":
                    next_layer.add((nr, pc + 1))
                elif ch == "]":
                    next_layer.add((nr, pc - 1))
                elif ch == "O":
                    pass  # single-width box

        if all_empty:
            break
        layers.append(next_layer)

    # Move layers from furthest to closest
    for layer in reversed(layers):
        for pr, pc in layer:
            grid[pr + dr][pc] = grid[pr][pc]
            grid[pr][pc] = "."

    return r + dr, c


def gps_sum(grid):
    total = 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in ("O", "["):
                total += 100 * r + c
    return total


def simulate(grid, moves):
    r, c = find_robot(grid)
    for move in moves:
        dr, dc = DIRS[move]
        if dc != 0:  # horizontal
            c = push_horizontal(grid, r, c, dc)
        else:  # vertical
            r, c = push_vertical(grid, r, c, dr)
    return grid


def solve(puzzle_input: str) -> tuple[str, str]:
    grid1, moves = parse_input(puzzle_input)
    grid2 = widen_grid(grid1)

    simulate(grid1, moves)
    part1 = gps_sum(grid1)

    simulate(grid2, moves)
    part2 = gps_sum(grid2)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    grid, moves = parse_input(puzzle_input)
    rows, cols = len(grid), len(grid[0])

    display_rows = min(20, rows)
    display_cols = min(40, cols)
    cells = []
    colors = {"#": "#666666", "O": "#ffaa00", "@": "#00ff41", ".": "#1a1a1a"}

    for r in range(display_rows):
        row = []
        for c in range(display_cols):
            row.append(grid[r][c])
        cells.append(row)

    yield {"type": "grid", "cells": cells, "colors": colors, "delay": 800}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Warehouse Woes",
            "  ===================================",
            "",
            f"  Grid: {rows} x {cols}",
            f"  Moves: {len(moves)}",
            f"  Part 1: {part1} (GPS sum)",
            f"  Part 2: {part2} (wide warehouse GPS)",
        ],
        "delay": 500,
    }
