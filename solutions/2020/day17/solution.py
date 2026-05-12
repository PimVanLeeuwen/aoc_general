"""
Day 17 - Conway Cubes
Year: 2020

3D and 4D cellular automaton using sparse sets to track active cubes.
"""

from itertools import product as cartesian
from collections import Counter


def simulate(active, dimensions, cycles=6):
    """Run the Conway Cubes automaton for the given number of cycles.

    Uses a sparse set of active coordinates and neighbor counting.
    """
    for _ in range(cycles):
        # Count neighbors for all cells adjacent to active ones
        neighbor_counts = Counter()
        deltas = [d for d in cartesian((-1, 0, 1), repeat=dimensions) if any(d)]
        for pos in active:
            for delta in deltas:
                neighbor = tuple(p + d for p, d in zip(pos, delta))
                neighbor_counts[neighbor] += 1

        new_active = set()
        # Active cells that survive
        for pos in active:
            if neighbor_counts.get(pos, 0) in (2, 3):
                new_active.add(pos)
        # Inactive cells that become active
        for pos, count in neighbor_counts.items():
            if count == 3 and pos not in active:
                new_active.add(pos)

        active = new_active

    return len(active)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    active_3d = set()
    active_4d = set()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "#":
                active_3d.add((x, y, 0))
                active_4d.add((x, y, 0, 0))

    part1 = simulate(active_3d, 3)
    part2 = simulate(active_4d, 4)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the Conway Cubes simulation."""
    lines = puzzle_input.strip().split("\n")

    active_3d = set()
    active_4d = set()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "#":
                active_3d.add((x, y, 0))
                active_4d.add((x, y, 0, 0))

    initial = len(active_3d)

    yield {
        "type": "text",
        "lines": [
            "  Conway Cubes",
            "",
            f"  Initial grid: {len(lines[0])}x{len(lines)}",
            f"  Initial active cubes: {initial}",
            "",
            "  Simulating 6 cycles in 3D and 4D...",
        ],
        "delay": 600,
    }

    part1 = simulate(active_3d, 3)
    part2 = simulate(active_4d, 4)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} active cubes (3D)",
            f"  Part 2: {part2} active cubes (4D)",
        ],
        "delay": 500,
    }
