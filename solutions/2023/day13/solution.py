"""
Day 13 - Point of Incidence
Year: 2023

Find horizontal and vertical reflection lines in ash/rock patterns,
then find the smudged reflection with exactly one bit difference.
"""


def find_reflection(rows, required_diffs=0):
    """Find a reflection line with exactly `required_diffs` total mismatches."""
    for i in range(1, len(rows)):
        diffs = 0
        for a, b in zip(rows[i - 1 :: -1], rows[i:]):
            diffs += sum(x != y for x, y in zip(a, b))
            if diffs > required_diffs:
                break
        if diffs == required_diffs:
            return i
    return 0


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    patterns = puzzle_input.strip().split("\n\n")
    part1 = 0
    part2 = 0

    for pattern in patterns:
        rows = pattern.split("\n")
        cols = ["".join(rows[r][c] for r in range(len(rows))) for c in range(len(rows[0]))]

        # Part 1: perfect reflection
        part1 += 100 * find_reflection(rows, 0)
        part1 += find_reflection(cols, 0)

        # Part 2: reflection with exactly one smudge
        part2 += 100 * find_reflection(rows, 1)
        part2 += find_reflection(cols, 1)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing reflection patterns."""
    patterns = puzzle_input.strip().split("\n\n")

    yield {
        "type": "text",
        "lines": [
            "  Point of Incidence",
            "",
            f"  Patterns: {len(patterns)}",
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
            f"  Part 1: {part1} (perfect reflections)",
            f"  Part 2: {part2} (with smudge fix)",
        ],
        "delay": 500,
    }
