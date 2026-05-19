"""
Day 19 - Aplenty
Year: 2023

Process parts through conditional workflows, then count
all accepted rating combinations using range splitting.
"""


def parse_workflows(text):
    """Parse workflow definitions into a dict of rule lists."""
    workflows = {}
    for line in text.split("\n"):
        name, rest = line.split("{")
        rules = []
        for rule in rest[:-1].split(","):
            if ":" in rule:
                condition, target = rule.split(":")
                cat = condition[0]
                op = condition[1]
                val = int(condition[2:])
                rules.append((cat, op, val, target))
            else:
                rules.append((None, None, None, rule))
        workflows[name] = rules
    return workflows


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    workflow_text, parts_text = puzzle_input.strip().split("\n\n")
    workflows = parse_workflows(workflow_text)

    # Part 1: process individual parts
    part1 = 0
    for line in parts_text.split("\n"):
        ratings = {}
        for item in line[1:-1].split(","):
            cat, val = item.split("=")
            ratings[cat] = int(val)

        state = "in"
        while state not in ("A", "R"):
            for cat, op, val, target in workflows[state]:
                if cat is None:
                    state = target
                    break
                rating = ratings[cat]
                if (op == "<" and rating < val) or (op == ">" and rating > val):
                    state = target
                    break

        if state == "A":
            part1 += sum(ratings.values())

    # Part 2: count all accepted combinations using range splitting
    # Each range is {cat: (lo, hi)} where lo..hi is inclusive
    def count_accepted(state, ranges):
        if state == "R":
            return 0
        if state == "A":
            result = 1
            for lo, hi in ranges.values():
                result *= hi - lo + 1
            return result

        total = 0
        ranges = dict(ranges)  # copy to avoid mutation

        for cat, op, val, target in workflows[state]:
            if cat is None:
                total += count_accepted(target, ranges)
                break

            lo, hi = ranges[cat]
            if op == "<":
                if hi < val:  # entire range passes
                    total += count_accepted(target, ranges)
                    break
                elif lo < val:  # split
                    new_ranges = dict(ranges)
                    new_ranges[cat] = (lo, val - 1)
                    total += count_accepted(target, new_ranges)
                    ranges[cat] = (val, hi)
                # else: entire range fails, continue to next rule
            else:  # op == ">"
                if lo > val:  # entire range passes
                    total += count_accepted(target, ranges)
                    break
                elif hi > val:  # split
                    new_ranges = dict(ranges)
                    new_ranges[cat] = (val + 1, hi)
                    total += count_accepted(target, new_ranges)
                    ranges[cat] = (lo, val)
                # else: entire range fails, continue to next rule

        return total

    initial_ranges = {c: (1, 4000) for c in "xmas"}
    part2 = count_accepted("in", initial_ranges)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing workflow processing."""
    workflow_text, parts_text = puzzle_input.strip().split("\n\n")
    workflows = workflow_text.split("\n")
    parts = parts_text.split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Aplenty",
            "",
            f"  Workflows: {len(workflows)}",
            f"  Parts: {len(parts)}",
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
            f"  Part 1: {part1} (accepted parts)",
            f"  Part 2: {part2} (combinations)",
        ],
        "delay": 500,
    }
