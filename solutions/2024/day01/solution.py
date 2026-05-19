"""
Day 1 - Historian Hysteria
Year: 2024

Compare two lists of location IDs by pairing them up sorted
and computing a similarity score.
"""

from collections import Counter


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    left = []
    right = []
    for line in lines:
        parts = line.split()
        left.append(int(parts[0]))
        right.append(int(parts[1]))

    left.sort()
    right.sort()

    # Part 1: sum of absolute differences between paired elements
    part1 = sum(abs(a - b) for a, b in zip(left, right))

    # Part 2: similarity score — each left number * its count in right list
    right_counts = Counter(right)
    part2 = sum(n * right_counts[n] for n in left)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")

    left = []
    right = []
    for line in lines:
        parts = line.split()
        left.append(int(parts[0]))
        right.append(int(parts[1]))

    left.sort()
    right.sort()

    sample = list(zip(left[:8], right[:8]))
    text_lines = ["  Historian Hysteria", "", "  Sorted pairs (first 8):"]
    for a, b in sample:
        diff = abs(a - b)
        text_lines.append(f"  {a:6d}  {b:6d}  diff={diff}")

    yield {"type": "text", "lines": text_lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (total distance)",
            f"  Part 2: {part2} (similarity score)",
        ],
        "delay": 500,
    }
