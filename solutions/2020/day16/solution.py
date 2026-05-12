"""
Day 16 - Ticket Translation
Year: 2020

Parse ticket field rules, discard invalid nearby tickets, then determine
which field corresponds to which position using constraint elimination.
"""

import re
from math import prod


def parse_input(text):
    """Parse rules, your ticket, and nearby tickets."""
    sections = text.strip().split("\n\n")

    rules = {}
    for line in sections[0].split("\n"):
        name = line.split(":")[0]
        nums = list(map(int, re.findall(r"\d+", line)))
        rules[name] = ((nums[0], nums[1]), (nums[2], nums[3]))

    my_ticket = list(map(int, sections[1].split("\n")[1].split(",")))
    nearby = [
        list(map(int, line.split(",")))
        for line in sections[2].split("\n")[1:]
        if line.strip()
    ]

    return rules, my_ticket, nearby


def matches_any_rule(value, rules):
    """Check if a value is valid for at least one rule."""
    return any(
        lo1 <= value <= hi1 or lo2 <= value <= hi2
        for (lo1, hi1), (lo2, hi2) in rules.values()
    )


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rules, my_ticket, nearby = parse_input(puzzle_input)

    # Part 1: sum of all invalid values across nearby tickets
    error_rate = 0
    valid_tickets = []
    for ticket in nearby:
        invalid = [v for v in ticket if not matches_any_rule(v, rules)]
        if invalid:
            error_rate += sum(invalid)
        else:
            valid_tickets.append(ticket)

    # Part 2: determine field positions
    # For each position, start with all possible field names
    n = len(my_ticket)
    possible = [set(rules.keys()) for _ in range(n)]

    # Eliminate fields that don't match any valid ticket at each position
    for ticket in valid_tickets:
        for i, value in enumerate(ticket):
            for name, ((lo1, hi1), (lo2, hi2)) in rules.items():
                if not (lo1 <= value <= hi1 or lo2 <= value <= hi2):
                    possible[i].discard(name)

    # Iteratively assign fields with only one possibility
    assigned = {}
    while len(assigned) < n:
        for i in range(n):
            if i in assigned:
                continue
            if len(possible[i]) == 1:
                name = next(iter(possible[i]))
                assigned[i] = name
                for j in range(n):
                    possible[j].discard(name)

    part2 = prod(
        my_ticket[i] for i, name in assigned.items()
        if name.startswith("departure")
    )

    return str(error_rate), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing ticket validation and field assignment."""
    rules, my_ticket, nearby = parse_input(puzzle_input)

    error_rate = 0
    valid_count = 0
    for ticket in nearby:
        invalid = [v for v in ticket if not matches_any_rule(v, rules)]
        if invalid:
            error_rate += sum(invalid)
        else:
            valid_count += 1

    yield {
        "type": "text",
        "lines": [
            "  Ticket Translation",
            "",
            f"  Field rules: {len(rules)}",
            f"  Nearby tickets: {len(nearby)}",
            f"  Valid tickets: {valid_count}",
            f"  Invalid tickets: {len(nearby) - valid_count}",
        ],
        "delay": 600,
    }

    _, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {error_rate} (ticket scanning error rate)",
            f"  Part 2: {part2} (departure fields product)",
        ],
        "delay": 500,
    }
