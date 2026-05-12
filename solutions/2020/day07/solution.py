"""
Day 7 - Handy Haversacks
Year: 2020

Parse bag containment rules to find which bags can hold a shiny gold bag
and how many bags a shiny gold bag must contain.
"""

import re
from collections import deque


def parse_rules(text):
    """Parse bag rules into a dict: bag_color -> [(count, inner_color), ...]."""
    rules = {}
    for line in text.strip().split("\n"):
        outer = re.match(r"(.+?) bags contain", line).group(1)
        inner = re.findall(r"(\d+) (.+?) bags?", line)
        rules[outer] = [(int(n), color) for n, color in inner]
    return rules


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    rules = parse_rules(puzzle_input)

    # Part 1: which bags can eventually contain a shiny gold bag?
    # Build reverse lookup: inner -> set of outers
    contained_by = {}
    for outer, contents in rules.items():
        for _, inner in contents:
            contained_by.setdefault(inner, set()).add(outer)

    can_hold = set()
    queue = deque(contained_by.get("shiny gold", []))
    while queue:
        bag = queue.popleft()
        if bag not in can_hold:
            can_hold.add(bag)
            queue.extend(contained_by.get(bag, []))

    # Part 2: how many bags inside a shiny gold bag?
    # BFS with multiplied counts
    total = 0
    queue = deque([(1, "shiny gold")])
    while queue:
        count, bag = queue.popleft()
        total += count
        for n, inner in rules.get(bag, []):
            queue.append((count * n, inner))
    total -= 1  # exclude the shiny gold bag itself

    return str(len(can_hold)), str(total)


def visualize(puzzle_input: str):
    """Yield frames showing bag containment analysis."""
    rules = parse_rules(puzzle_input)

    contained_by = {}
    for outer, contents in rules.items():
        for _, inner in contents:
            contained_by.setdefault(inner, set()).add(outer)

    can_hold = set()
    queue = deque(contained_by.get("shiny gold", []))
    while queue:
        bag = queue.popleft()
        if bag not in can_hold:
            can_hold.add(bag)
            queue.extend(contained_by.get(bag, []))

    total = 0
    queue = deque([(1, "shiny gold")])
    while queue:
        count, bag = queue.popleft()
        total += count
        for n, inner in rules.get(bag, []):
            queue.append((count * n, inner))
    total -= 1

    yield {
        "type": "text",
        "lines": [
            "  Handy Haversacks",
            "",
            f"  Bag rules: {len(rules)}",
            f"  Direct containers of shiny gold: {len(contained_by.get('shiny gold', []))}",
            "",
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {len(can_hold)} bags can contain shiny gold",
            f"  Part 2: {total} bags inside shiny gold",
        ],
        "delay": 500,
    }
