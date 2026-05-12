"""
Day 19 - Monster Messages
Year: 2020

Match messages against recursive grammar rules by compiling them into
regular expressions.
"""

import re


def build_regex(rules, rule_id=0, depth=0):
    """Recursively build a regex string from the grammar rules.

    depth limit prevents infinite recursion for Part 2's self-referencing rules.
    """
    if depth > 15:
        return ""

    rule = rules[rule_id]

    if rule.startswith('"'):
        return rule[1]

    options = rule.split(" | ")
    parts = []
    for option in options:
        sub = "".join(
            build_regex(rules, int(r), depth + 1) for r in option.split()
        )
        parts.append(sub)

    if len(parts) == 1:
        return parts[0]
    return "(?:" + "|".join(parts) + ")"


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    sections = puzzle_input.strip().split("\n\n")

    rules = {}
    for line in sections[0].split("\n"):
        idx, body = line.split(": ")
        rules[int(idx)] = body

    messages = sections[1].split("\n")

    # Part 1: compile rule 0 into a regex
    pattern1 = re.compile("^" + build_regex(rules) + "$")
    part1 = sum(1 for m in messages if pattern1.match(m))

    # Part 2: patch rules 8 and 11 to be self-referencing
    #   8: 42 | 42 8        → 42+
    #   11: 42 31 | 42 11 31 → 42{n} 31{n} for some n (manually unroll)
    rules2 = dict(rules)
    rules2[8] = "42 | 42 8"
    rules2[11] = "42 31 | 42 11 31"

    pattern2 = re.compile("^" + build_regex(rules2) + "$")
    part2 = sum(1 for m in messages if pattern2.match(m))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing message matching."""
    sections = puzzle_input.strip().split("\n\n")

    rules = {}
    for line in sections[0].split("\n"):
        idx, body = line.split(": ")
        rules[int(idx)] = body

    messages = sections[1].split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Monster Messages",
            "",
            f"  Grammar rules: {len(rules)}",
            f"  Messages to check: {len(messages)}",
            f"  Message lengths: {min(len(m) for m in messages)}-{max(len(m) for m in messages)}",
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
            f"  Part 1: {part1} messages match rule 0",
            f"  Part 2: {part2} messages match (with loops)",
        ],
        "delay": 500,
    }
