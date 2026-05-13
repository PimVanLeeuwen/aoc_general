"""
Day 4 - Camp Cleanup
Year: 2022

Count assignment pairs where one range fully contains the other,
and pairs where the ranges overlap at all.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    contains = 0
    overlaps = 0

    for line in puzzle_input.strip().split("\n"):
        a, b, c, d = map(int, line.replace(",", "-").split("-"))

        if (a <= c and b >= d) or (c <= a and d >= b):
            contains += 1
        if a <= d and c <= b:
            overlaps += 1

    return str(contains), str(overlaps)


def visualize(puzzle_input: str):
    """Yield frames showing range overlaps."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Camp Cleanup",
            "",
            f"  Assignment pairs: {len(lines)}",
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
            f"  Part 1: {part1} (fully contained)",
            f"  Part 2: {part2} (any overlap)",
        ],
        "delay": 500,
    }
