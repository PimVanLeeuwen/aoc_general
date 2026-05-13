"""
Day 3 - Rucksack Reorganization
Year: 2022

Find misplaced items by set intersection on rucksack compartments
and elf group badges.
"""


def priority(ch):
    """Return priority: a-z → 1-26, A-Z → 27-52."""
    if ch.islower():
        return ord(ch) - ord("a") + 1
    return ord(ch) - ord("A") + 27


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    # Part 1: shared item between two halves
    part1 = 0
    for line in lines:
        mid = len(line) // 2
        common = set(line[:mid]) & set(line[mid:])
        part1 += priority(common.pop())

    # Part 2: badge shared across groups of 3
    part2 = 0
    for i in range(0, len(lines), 3):
        badge = set(lines[i]) & set(lines[i + 1]) & set(lines[i + 2])
        part2 += priority(badge.pop())

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing rucksack analysis."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Rucksack Reorganization",
            "",
            f"  Rucksacks: {len(lines)}",
            f"  Groups: {len(lines) // 3}",
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
            f"  Part 1: {part1} (misplaced items)",
            f"  Part 2: {part2} (group badges)",
        ],
        "delay": 500,
    }
