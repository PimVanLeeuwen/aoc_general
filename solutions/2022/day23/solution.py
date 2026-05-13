"""
Day 23 - Unstable Diffusion
Year: 2022

Simulate elves spreading out by proposing moves in
rotating priority directions.
"""

from collections import defaultdict


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    elves = set()
    for y, line in enumerate(puzzle_input.strip().split("\n")):
        for x, ch in enumerate(line):
            if ch == "#":
                elves.add((x, y))

    # Direction groups: N, S, W, E
    checks = [
        [(-1, -1), (0, -1), (1, -1)],  # N
        [(-1, 1), (0, 1), (1, 1)],     # S
        [(-1, -1), (-1, 0), (-1, 1)],  # W
        [(1, -1), (1, 0), (1, 1)],     # E
    ]
    # Movement direction for each group (center of the 3 checked positions)
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    all_adj = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    part1 = ""
    dir_start = 0

    for rnd in range(10000):
        proposals = defaultdict(list)

        for x, y in elves:
            if not any((x + dx, y + dy) in elves for dx, dy in all_adj):
                continue

            for i in range(4):
                di = (dir_start + i) % 4
                if all((x + dx, y + dy) not in elves for dx, dy in checks[di]):
                    dx, dy = moves[di]
                    proposals[(x + dx, y + dy)].append((x, y))
                    break

        new_elves = set(elves)
        moved = False
        for dest, sources in proposals.items():
            if len(sources) == 1:
                new_elves.remove(sources[0])
                new_elves.add(dest)
                moved = True

        if rnd == 9:
            min_x = min(e[0] for e in new_elves)
            max_x = max(e[0] for e in new_elves)
            min_y = min(e[1] for e in new_elves)
            max_y = max(e[1] for e in new_elves)
            part1 = str((max_x - min_x + 1) * (max_y - min_y + 1) - len(new_elves))

        if not moved:
            part2 = str(rnd + 1)
            return part1 if part1 else "0", part2

        elves = new_elves
        dir_start = (dir_start + 1) % 4

    return part1, ""


def visualize(puzzle_input: str):
    """Yield frames showing elf positions."""
    elves = set()
    for y, line in enumerate(puzzle_input.strip().split("\n")):
        for x, ch in enumerate(line):
            if ch == "#":
                elves.add((x, y))

    yield {
        "type": "text",
        "lines": [
            "  Unstable Diffusion",
            "",
            f"  Elves: {len(elves)}",
        ],
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (empty tiles after 10)",
            f"  Part 2: {part2} (first no-move round)",
        ],
        "delay": 500,
    }
