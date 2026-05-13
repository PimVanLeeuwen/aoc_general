"""
Day 11 - Monkey in the Middle
Year: 2022

Simulate monkeys throwing items based on worry-level operations
and divisibility tests.
"""

import re
from math import prod


def parse_monkeys(text):
    """Parse monkey definitions from input."""
    monkeys = []
    for block in text.strip().split("\n\n"):
        lines = block.strip().split("\n")
        items = list(map(int, re.findall(r"\d+", lines[1])))
        op_parts = lines[2].split("= ")[1]
        divisor = int(re.findall(r"\d+", lines[3])[0])
        true_target = int(re.findall(r"\d+", lines[4])[0])
        false_target = int(re.findall(r"\d+", lines[5])[0])
        monkeys.append({
            "items": items,
            "op": op_parts,
            "div": divisor,
            "true": true_target,
            "false": false_target,
        })
    return monkeys


def apply_op(op_str, old):
    """Evaluate the operation string with the given old value."""
    a, operator, b = op_str.split()
    a = old if a == "old" else int(a)
    b = old if b == "old" else int(b)
    return a + b if operator == "+" else a * b


def simulate(monkeys, rounds, relief):
    """Run the simulation and return inspection counts."""
    items = [list(m["items"]) for m in monkeys]
    counts = [0] * len(monkeys)
    mod = prod(m["div"] for m in monkeys)

    for _ in range(rounds):
        for i, m in enumerate(monkeys):
            for item in items[i]:
                counts[i] += 1
                worry = apply_op(m["op"], item)
                if relief:
                    worry //= 3
                else:
                    worry %= mod
                target = m["true"] if worry % m["div"] == 0 else m["false"]
                items[target].append(worry)
            items[i] = []

    counts.sort(reverse=True)
    return counts[0] * counts[1]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    monkeys = parse_monkeys(puzzle_input)

    part1 = simulate(monkeys, 20, relief=True)
    part2 = simulate(monkeys, 10000, relief=False)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing monkey business."""
    monkeys = parse_monkeys(puzzle_input)

    lines = ["  Monkey in the Middle", ""]
    for i, m in enumerate(monkeys):
        lines.append(f"  Monkey {i}: items {m['items']}, test div {m['div']}")

    yield {"type": "text", "lines": lines, "delay": 600}

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (20 rounds, /3 relief)",
            f"  Part 2: {part2} (10000 rounds, mod relief)",
        ],
        "delay": 500,
    }
