"""
Day 20 - Jurassic Jigsaw
Year: 2020

Assemble image tiles by matching edges, then search for sea monsters
in the composed image across all orientations.
"""

from math import isqrt, prod
from collections import defaultdict


def parse_tiles(text):
    """Parse tiles into a dict of {tile_id: grid (list of strings)}."""
    tiles = {}
    for block in text.strip().split("\n\n"):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        header = lines[0].strip()
        tile_id = int(header.split()[1].rstrip(":"))
        grid = [line.strip() for line in lines[1:] if line.strip()]
        tiles[tile_id] = grid
    return tiles


def edges(grid):
    """Return the 4 edges of a grid: top, right, bottom, left."""
    top = grid[0]
    bottom = grid[-1]
    left = "".join(row[0] for row in grid)
    right = "".join(row[-1] for row in grid)
    return (top, right, bottom, left)


def rotate(grid):
    """Rotate a grid 90 degrees clockwise."""
    n = len(grid)
    return ["".join(grid[n - 1 - j][i] for j in range(n)) for i in range(n)]


def flip_h(grid):
    """Flip a grid horizontally."""
    return [row[::-1] for row in grid]


def orientations(grid):
    """Yield all 8 orientations (4 rotations x 2 flips) of a grid."""
    g = list(grid)
    for _ in range(4):
        yield g
        yield flip_h(g)
        g = rotate(g)


def crop(grid):
    """Remove the border of a tile grid."""
    return [row[1:-1] for row in grid[1:-1]]


def assemble(tiles):
    """Assemble tiles into a complete image. Returns (part1, image_grid)."""
    # Map each canonical edge to the tiles that share it
    edge_to_tiles = defaultdict(set)
    for tid, grid in tiles.items():
        for e in edges(grid):
            canon = min(e, e[::-1])
            edge_to_tiles[canon].add(tid)

    # Build neighbor map
    neighbors = defaultdict(set)
    for tids in edge_to_tiles.values():
        if len(tids) == 2:
            a, b = tids
            neighbors[a].add(b)
            neighbors[b].add(a)

    # Corners have exactly 2 neighbors
    corners = [tid for tid in tiles if len(neighbors[tid]) == 2]
    part1 = prod(corners)

    # Place tiles in a grid
    size = isqrt(len(tiles))
    placed = [[None] * size for _ in range(size)]
    used = set()

    def has_neighbor(tid, edge_str):
        """Check if a tile edge matches another tile."""
        canon = min(edge_str, edge_str[::-1])
        return len(edge_to_tiles[canon] - {tid}) > 0

    # Start with a corner, oriented so shared edges face right and down
    start = corners[0]
    for o in orientations(tiles[start]):
        e = edges(o)
        if has_neighbor(start, e[1]) and has_neighbor(start, e[2]):
            placed[0][0] = (start, o)
            used.add(start)
            break

    # Fill the grid row by row
    for row in range(size):
        for col in range(size):
            if placed[row][col] is not None:
                continue

            if col > 0:
                # Match left edge to right edge of left neighbor
                need = edges(placed[row][col - 1][1])[1]
                edge_idx = 3  # left edge of candidate
            else:
                # Match top edge to bottom edge of top neighbor
                need = edges(placed[row - 1][col][1])[2]
                edge_idx = 0  # top edge of candidate

            for tid, grid in tiles.items():
                if tid in used:
                    continue
                found = False
                for o in orientations(grid):
                    if edges(o)[edge_idx] == need:
                        placed[row][col] = (tid, o)
                        used.add(tid)
                        found = True
                        break
                if found:
                    break

    # Stitch cropped tiles into the full image
    image = []
    for row in range(size):
        cropped = [crop(placed[row][col][1]) for col in range(size)]
        for r in range(len(cropped[0])):
            image.append("".join(c[r] for c in cropped))

    return part1, image


SEA_MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #  ",
]
# Pad all rows to the same width
_mw = max(len(row) for row in SEA_MONSTER)
SEA_MONSTER = [row.ljust(_mw) for row in SEA_MONSTER]


def count_monsters(image):
    """Count sea monsters in the image."""
    mh = len(SEA_MONSTER)
    mw = len(SEA_MONSTER[0])
    monster_coords = [
        (r, c)
        for r in range(mh)
        for c in range(mw)
        if SEA_MONSTER[r][c] == "#"
    ]

    h = len(image)
    w = len(image[0]) if image else 0
    count = 0
    for r in range(h - mh + 1):
        for c in range(w - mw + 1):
            if all(image[r + dr][c + dc] == "#" for dr, dc in monster_coords):
                count += 1
    return count


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    tiles = parse_tiles(puzzle_input)
    part1, image = assemble(tiles)

    # Try all orientations to find sea monsters
    total_hash = sum(row.count("#") for row in image)
    monster_cells = sum(row.count("#") for row in SEA_MONSTER)

    for oriented in orientations(image):
        monsters = count_monsters(oriented)
        if monsters > 0:
            part2 = total_hash - monsters * monster_cells
            break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing tile assembly and sea monster search."""
    tiles = parse_tiles(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Jurassic Jigsaw",
            "",
            f"  Tiles: {len(tiles)}",
            f"  Grid: {isqrt(len(tiles))}x{isqrt(len(tiles))}",
            f"  Tile size: {len(next(iter(tiles.values())))}x{len(next(iter(tiles.values()))[0])}",
        ],
        "delay": 600,
    }

    part1, image = assemble(tiles)

    # Show assembled image
    cells = [
        ["#" if ch == "#" else "." for ch in row]
        for row in image
    ]

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {
            ".": "#0f0f23",
            "#": "#666688",
        },
        "delay": 800,
    }

    total_hash = sum(row.count("#") for row in image)
    monster_cells = sum(row.count("#") for row in SEA_MONSTER)
    monsters = 0
    part2 = 0
    for oriented in orientations(image):
        monsters = count_monsters(oriented)
        if monsters > 0:
            part2 = total_hash - monsters * monster_cells
            break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (corner ID product)",
            f"  Part 2: {part2} (water roughness)",
            f"    Sea monsters found: {monsters}",
            f"    Monster cells: {monster_cells} each",
        ],
        "delay": 500,
    }
