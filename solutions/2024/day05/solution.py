"""
Day 5 - Print Queue
Year: 2024

Validate page ordering rules and fix incorrectly ordered
updates using topological sorting.
"""

from collections import defaultdict


def is_valid_order(pages, rules):
    """Check if pages satisfy all applicable ordering rules."""
    position = {page: i for i, page in enumerate(pages)}
    for before, after in rules:
        if before in position and after in position:
            if position[before] > position[after]:
                return False
    return True


def fix_order(pages, rules):
    """Reorder pages to satisfy all applicable rules via repeated swaps."""
    pages = list(pages)
    changed = True
    while changed:
        changed = False
        position = {page: i for i, page in enumerate(pages)}
        for before, after in rules:
            if before in position and after in position:
                if position[before] > position[after]:
                    i, j = position[before], position[after]
                    pages[i], pages[j] = pages[j], pages[i]
                    changed = True
                    break
    return pages


def solve(puzzle_input: str) -> tuple[str, str]:
    sections = puzzle_input.strip().split("\n\n")
    rule_lines = sections[0].split("\n")
    update_lines = sections[1].split("\n")

    rules = []
    for line in rule_lines:
        a, b = line.split("|")
        rules.append((int(a), int(b)))

    part1 = 0
    part2 = 0

    for line in update_lines:
        pages = list(map(int, line.split(",")))
        if is_valid_order(pages, rules):
            part1 += pages[len(pages) // 2]
        else:
            fixed = fix_order(pages, rules)
            part2 += fixed[len(fixed) // 2]

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    sections = puzzle_input.strip().split("\n\n")
    rule_lines = sections[0].split("\n")
    update_lines = sections[1].split("\n")

    rules = []
    for line in rule_lines:
        a, b = line.split("|")
        rules.append((int(a), int(b)))

    valid = 0
    invalid = 0
    for line in update_lines:
        pages = list(map(int, line.split(",")))
        if is_valid_order(pages, rules):
            valid += 1
        else:
            invalid += 1

    yield {
        "type": "text",
        "lines": [
            "  Print Queue",
            "",
            f"  Ordering rules: {len(rules)}",
            f"  Updates: {len(update_lines)}",
            f"  Already valid: {valid}",
            f"  Need fixing: {invalid}",
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
            f"  Part 1: {part1} (valid middle pages)",
            f"  Part 2: {part2} (fixed middle pages)",
        ],
        "delay": 500,
    }
