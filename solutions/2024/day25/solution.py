"""
Day 25 - Code Chronicle
Year: 2024

Match locks and keys by checking if their pin heights
don't overlap in any column.
"""


def parse_schematics(text):
    locks = []
    keys = []

    for block in text.strip().split("\n\n"):
        rows = block.split("\n")
        heights = []
        for c in range(len(rows[0])):
            count = sum(1 for r in rows if rows[r][c] == "#") if False else sum(1 for row in rows if row[c] == "#")
            heights.append(count)

        if rows[0][0] == "#":
            locks.append(heights)
        else:
            keys.append(heights)

    return locks, keys


def solve(puzzle_input: str) -> tuple[str, str]:
    locks, keys = parse_schematics(puzzle_input)

    # Count lock/key pairs that fit (no column exceeds the schematic height)
    max_height = len(puzzle_input.strip().split("\n\n")[0].split("\n"))
    fits = 0

    for lock in locks:
        for key in keys:
            if all(lock[c] + key[c] <= max_height for c in range(len(lock))):
                fits += 1

    return str(fits), "Merry Christmas!"


def visualize(puzzle_input: str):
    locks, keys = parse_schematics(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Code Chronicle",
            "",
            f"  Locks: {len(locks)}",
            f"  Keys: {len(keys)}",
            f"  Combinations to check: {len(locks) * len(keys)}",
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
            f"  Part 1: {part1} (fitting pairs)",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
