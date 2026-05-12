"""
Day 24 - Planet of Discord
Year: 2019

Cellular automaton on a 5x5 grid. Part 1 finds the first repeated state.
Part 2 adds recursive depth levels with the center tile acting as a portal.
"""


def parse_grid(text):
    """Parse the 5x5 grid into a frozenset of bug positions."""
    bugs = set()
    for y, line in enumerate(text.strip().split("\n")):
        for x, ch in enumerate(line):
            if ch == "#":
                bugs.add((x, y))
    return frozenset(bugs)


def step_flat(bugs):
    """One step of the flat 5x5 automaton."""
    new = set()
    for y in range(5):
        for x in range(5):
            adj = sum(
                1 for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                if (x + dx, y + dy) in bugs
            )
            if (x, y) in bugs:
                if adj == 1:
                    new.add((x, y))
            else:
                if adj in (1, 2):
                    new.add((x, y))
    return frozenset(new)


def biodiversity(bugs):
    """Calculate biodiversity rating from bug positions."""
    return sum(1 << (y * 5 + x) for x, y in bugs)


def part1(bugs):
    """Find first repeated layout and return its biodiversity rating."""
    seen = set()
    while bugs not in seen:
        seen.add(bugs)
        bugs = step_flat(bugs)
    return biodiversity(bugs)


# Part 2: recursive levels. Center tile (2,2) is the portal to inner/outer levels.
# Adjacency rules for tiles next to the center (2,2):
#   (2,1) looks down into level+1 top row: (0,0),(1,0),(2,0),(3,0),(4,0)
#   (2,3) looks up into level+1 bottom row: (0,4),(1,4),(2,4),(3,4),(4,4)
#   (1,2) looks right into level+1 left col: (0,0),(0,1),(0,2),(0,3),(0,4)
#   (3,2) looks left into level+1 right col: (4,0),(4,1),(4,2),(4,3),(4,4)
# Edge tiles look outward to level-1:
#   top row (y=0) looks up to (2,1) at level-1
#   bottom row (y=4) looks down to (2,3) at level-1
#   left col (x=0) looks left to (1,2) at level-1
#   right col (x=4) looks right to (3,2) at level-1

def neighbors_recursive(x, y, level):
    """Yield (x, y, level) for all neighbors of (x, y, level) in recursive grid."""
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy

        # Moving to center tile -> recurse inward
        if nx == 2 and ny == 2:
            if dx == 1:  # entering from left
                for iy in range(5):
                    yield (0, iy, level + 1)
            elif dx == -1:  # entering from right
                for iy in range(5):
                    yield (4, iy, level + 1)
            elif dy == 1:  # entering from above
                for ix in range(5):
                    yield (ix, 0, level + 1)
            elif dy == -1:  # entering from below
                for ix in range(5):
                    yield (ix, 4, level + 1)
        # Moving outside grid -> recurse outward
        elif nx < 0:
            yield (1, 2, level - 1)
        elif nx > 4:
            yield (3, 2, level - 1)
        elif ny < 0:
            yield (2, 1, level - 1)
        elif ny > 4:
            yield (2, 3, level - 1)
        else:
            yield (nx, ny, level)


def step_recursive(bugs):
    """One step of the recursive automaton."""
    # Count neighbors for all cells that could change
    candidates = set()
    for bx, by, bl in bugs:
        candidates.add((bx, by, bl))
        for n in neighbors_recursive(bx, by, bl):
            candidates.add(n)

    new = set()
    for x, y, level in candidates:
        if x == 2 and y == 2:
            continue  # center is always the portal
        adj = sum(1 for n in neighbors_recursive(x, y, level) if n in bugs)
        if (x, y, level) in bugs:
            if adj == 1:
                new.add((x, y, level))
        else:
            if adj in (1, 2):
                new.add((x, y, level))
    return frozenset(new)


def part2(bugs_2d, minutes=200):
    """Run recursive automaton for given minutes, return total bug count."""
    bugs = frozenset((x, y, 0) for x, y in bugs_2d)
    for _ in range(minutes):
        bugs = step_recursive(bugs)
    return len(bugs)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    bugs = parse_grid(puzzle_input)

    p1 = part1(bugs)
    p2 = part2(bugs)

    return str(p1), str(p2)


def visualize(puzzle_input: str):
    """Yield frames showing the bug automaton."""
    bugs = parse_grid(puzzle_input)

    # Show initial state
    cells = []
    for y in range(5):
        row = []
        for x in range(5):
            row.append("#" if (x, y) in bugs else ".")
        cells.append(row)

    yield {
        "type": "grid",
        "cells": cells,
        "colors": {"#": "#00ff41", ".": "#0f0f23"},
        "delay": 600,
    }

    # Animate flat automaton until repeat
    seen = set()
    current = bugs
    gen = 0
    while current not in seen:
        seen.add(current)
        current = step_flat(current)
        gen += 1
        if gen <= 20 or gen % 10 == 0:
            cells = []
            for y in range(5):
                row = []
                for x in range(5):
                    row.append("#" if (x, y) in current else ".")
                cells.append(row)
            yield {
                "type": "grid",
                "cells": cells,
                "colors": {"#": "#00ff41", ".": "#0f0f23"},
                "delay": 150,
            }

    p1 = biodiversity(current)

    yield {
        "type": "text",
        "lines": [
            "  Planet of Discord",
            "",
            f"  First repeat at generation {gen}",
            f"  Biodiversity rating: {p1}",
            "",
            "  Running recursive simulation (200 min)...",
        ],
        "delay": 600,
    }

    p2 = part2(bugs)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {p1} (first repeated biodiversity)",
            f"  Part 2: {p2} (bugs after 200 recursive min)",
        ],
        "delay": 500,
    }
