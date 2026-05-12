"""
Day 6 - Custom Customs
Year: 2020

Count yes-answers from groups of travellers — anyone vs everyone.
"""

from functools import reduce


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    groups = puzzle_input.strip().split("\n\n")

    part1 = part2 = 0
    for group in groups:
        people = [set(person) for person in group.split("\n")]
        part1 += len(reduce(set.union, people))
        part2 += len(reduce(set.intersection, people))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing customs form analysis."""
    groups = puzzle_input.strip().split("\n\n")

    anyone_total = everyone_total = 0
    for group in groups:
        people = [set(person) for person in group.split("\n")]
        anyone_total += len(reduce(set.union, people))
        everyone_total += len(reduce(set.intersection, people))

    sizes = [len(g.split("\n")) for g in groups]

    yield {
        "type": "text",
        "lines": [
            "  Custom Customs",
            "",
            f"  Groups: {len(groups)}",
            f"  People: {sum(sizes)}",
            f"  Largest group: {max(sizes)} people",
            "",
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {anyone_total} (anyone answered yes)",
            f"  Part 2: {everyone_total} (everyone answered yes)",
        ],
        "delay": 500,
    }
