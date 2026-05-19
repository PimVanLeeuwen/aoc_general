"""
Day 4 - Scratchcards
Year: 2023

Score scratchcards by matching numbers, then cascade
card copies based on match counts.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    n = len(lines)
    copies = [1] * n
    part1 = 0

    for i, line in enumerate(lines):
        _, cards = line.split(": ")
        winning, own = cards.split(" | ")
        winning = set(winning.split())
        own = own.split()

        matches = sum(1 for num in own if num in winning)

        # Part 1: doubling score
        if matches > 0:
            part1 += 1 << (matches - 1)

        # Part 2: cascade copies
        for j in range(matches):
            if i + 1 + j < n:
                copies[i + 1 + j] += copies[i]

    part2 = sum(copies)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing scratchcard processing."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Scratchcards",
            "",
            f"  Cards: {len(lines)}",
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
            f"  Part 1: {part1} (point total)",
            f"  Part 2: {part2} (total cards)",
        ],
        "delay": 500,
    }
