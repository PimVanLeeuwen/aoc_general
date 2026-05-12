"""
Day 24 - Lobby Layout
Year: 2020

Navigate a hex grid to flip tiles, then simulate a cellular automaton
on the hex grid for 100 days.
"""

from collections import Counter

# Hex grid using cube coordinates (axial: q, r)
# e/w move along q, se/nw move along r, ne/sw move along both
HEX_DIRS = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (0, 1),
    "nw": (0, -1),
    "ne": (1, -1),
    "sw": (-1, 1),
}


def parse_directions(line):
    """Parse a line of directions into a list of hex moves."""
    moves = []
    i = 0
    while i < len(line):
        if line[i] in ("e", "w"):
            moves.append(line[i])
            i += 1
        else:
            moves.append(line[i:i + 2])
            i += 2
    return moves


def follow_path(moves):
    """Follow hex directions and return the final coordinate."""
    q, r = 0, 0
    for move in moves:
        dq, dr = HEX_DIRS[move]
        q += dq
        r += dr
    return (q, r)


def get_initial_black(lines):
    """Determine which tiles are black after all flips."""
    black = set()
    for line in lines:
        moves = parse_directions(line)
        pos = follow_path(moves)
        black ^= {pos}
    return black


def hex_neighbors(pos):
    """Return the 6 hex neighbors of a position."""
    q, r = pos
    return [(q + dq, r + dr) for dq, dr in HEX_DIRS.values()]


def simulate_day(black):
    """Run one day of the hex cellular automaton."""
    neighbor_counts = Counter()
    for pos in black:
        for nb in hex_neighbors(pos):
            neighbor_counts[nb] += 1

    new_black = set()
    for pos in black:
        count = neighbor_counts.get(pos, 0)
        if count == 1 or count == 2:
            new_black.add(pos)

    for pos, count in neighbor_counts.items():
        if pos not in black and count == 2:
            new_black.add(pos)

    return new_black


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    black = get_initial_black(lines)
    part1 = len(black)

    for _ in range(100):
        black = simulate_day(black)
    part2 = len(black)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing hex tile flipping and daily simulation."""
    lines = puzzle_input.strip().split("\n")

    black = get_initial_black(lines)

    yield {
        "type": "text",
        "lines": [
            "  Lobby Layout",
            "",
            f"  Instructions: {len(lines)}",
            f"  Initial black tiles: {len(black)}",
        ],
        "delay": 600,
    }

    # Show automaton progression at key days
    counts = [len(black)]
    for day in range(1, 101):
        black = simulate_day(black)
        if day <= 10 or day % 10 == 0:
            counts.append((day, len(black)))

    progress_lines = ["  Daily progression:", ""]
    for item in counts:
        if isinstance(item, tuple):
            day, count = item
            progress_lines.append(f"  Day {day:>3}: {count} black tiles")
        else:
            progress_lines.append(f"  Day   0: {item} black tiles")

    yield {
        "type": "text",
        "lines": progress_lines,
        "delay": 800,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {counts[0]} (initial black tiles)",
            f"  Part 2: {counts[-1][1]} (after 100 days)",
        ],
        "delay": 500,
    }
