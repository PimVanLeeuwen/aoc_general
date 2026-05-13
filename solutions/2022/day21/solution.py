"""
Day 21 - Monkey Math
Year: 2022

Evaluate a tree of monkey expressions, then solve for
a variable to make two branches equal.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    monkeys = {}
    for line in puzzle_input.strip().split("\n"):
        name, expr = line.split(": ")
        if expr.lstrip("-").isdigit():
            monkeys[name] = int(expr)
        else:
            parts = expr.split()
            monkeys[name] = (parts[0], parts[1], parts[2])

    # Part 1: evaluate root
    def evaluate(name):
        val = monkeys[name]
        if isinstance(val, int):
            return val
        a, op, b = val
        va, vb = evaluate(a), evaluate(b)
        if op == "+": return va + vb
        if op == "-": return va - vb
        if op == "*": return va * vb
        return va // vb

    part1 = evaluate("root")

    # Part 2: find humn value so root's two children are equal
    # Check which side depends on humn
    def depends_on_humn(name):
        if name == "humn":
            return True
        val = monkeys[name]
        if isinstance(val, int):
            return False
        return depends_on_humn(val[0]) or depends_on_humn(val[2])

    left, _, right = monkeys["root"]

    if depends_on_humn(left):
        target = evaluate(right)
        variable_side = left
    else:
        target = evaluate(left)
        variable_side = right

    # Walk down the tree, inverting operations to solve for humn
    def solve_for(name, target_val):
        if name == "humn":
            return target_val
        a, op, b = monkeys[name]
        a_depends = depends_on_humn(a)

        if a_depends:
            bv = evaluate(b)
            if op == "+": return solve_for(a, target_val - bv)
            if op == "-": return solve_for(a, target_val + bv)
            if op == "*": return solve_for(a, target_val // bv)
            return solve_for(a, target_val * bv)
        else:
            av = evaluate(a)
            if op == "+": return solve_for(b, target_val - av)
            if op == "-": return solve_for(b, av - target_val)
            if op == "*": return solve_for(b, target_val // av)
            return solve_for(b, av // target_val)

    part2 = solve_for(variable_side, target)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing monkey math."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Monkey Math",
            "",
            f"  Monkeys: {len(lines)}",
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
            f"  Part 1: {part1} (root yells)",
            f"  Part 2: {part2} (humn value)",
        ],
        "delay": 500,
    }
