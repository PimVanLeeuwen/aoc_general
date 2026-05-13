"""
Day 1 - Calorie Counting
Year: 2022

Find the elf carrying the most calories, and the top three combined.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    elves = [
        sum(int(line) for line in group.split("\n"))
        for group in puzzle_input.strip().split("\n\n")
    ]
    elves.sort(reverse=True)

    return str(elves[0]), str(sum(elves[:3]))


def visualize(puzzle_input: str):
    """Yield frames showing calorie distribution."""
    elves = sorted(
        [sum(int(line) for line in g.split("\n")) for g in puzzle_input.strip().split("\n\n")],
        reverse=True,
    )

    top = elves[:10]
    max_cal = max(top)
    lines = ["  Top 10 elves by calories:", ""]
    for i, cal in enumerate(top):
        bar = "#" * int(40 * cal / max_cal)
        marker = " <--" if i < 3 else ""
        lines.append(f"  {i + 1:>2}. {bar} {cal:,}{marker}")

    yield {"type": "text", "lines": lines, "delay": 600}

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {elves[0]} (top elf)",
            f"  Part 2: {sum(elves[:3])} (top 3 combined)",
        ],
        "delay": 500,
    }
