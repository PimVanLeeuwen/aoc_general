"""
Day 18 - Operation Order
Year: 2020

Evaluate arithmetic expressions with unusual precedence rules:
equal precedence (Part 1) and addition before multiplication (Part 2).
"""


def tokenize(expr):
    """Split an expression into number and operator tokens."""
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(int(expr[i:j]))
            i = j
        elif expr[i] in "+*()":
            tokens.append(expr[i])
            i += 1
        else:
            i += 1  # skip spaces
    return tokens


def eval_equal_precedence(tokens, pos=0):
    """Evaluate with + and * having equal precedence (left to right).

    Returns (result, next_position).
    """
    def parse_atom(p):
        if tokens[p] == "(":
            val, p = parse_expr(p + 1)
            return val, p + 1  # skip ')'
        return tokens[p], p + 1

    def parse_expr(p):
        val, p = parse_atom(p)
        while p < len(tokens) and tokens[p] in ("+", "*"):
            op = tokens[p]
            right, p = parse_atom(p + 1)
            val = val + right if op == "+" else val * right
        return val, p

    result, _ = parse_expr(pos)
    return result


def eval_addition_first(tokens, pos=0):
    """Evaluate with + having higher precedence than *.

    Returns (result, next_position).
    """
    def parse_atom(p):
        if tokens[p] == "(":
            val, p = parse_mul(p + 1)
            return val, p + 1  # skip ')'
        return tokens[p], p + 1

    def parse_add(p):
        val, p = parse_atom(p)
        while p < len(tokens) and tokens[p] == "+":
            right, p = parse_atom(p + 1)
            val += right
        return val, p

    def parse_mul(p):
        val, p = parse_add(p)
        while p < len(tokens) and tokens[p] == "*":
            right, p = parse_add(p + 1)
            val *= right
        return val, p

    result, _ = parse_mul(pos)
    return result


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    part1 = sum(eval_equal_precedence(tokenize(line)) for line in lines)
    part2 = sum(eval_addition_first(tokenize(line)) for line in lines)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing expression evaluation."""
    lines = puzzle_input.strip().split("\n")

    yield {
        "type": "text",
        "lines": [
            "  Operation Order",
            "",
            f"  Expressions: {len(lines)}",
            f"  Example: {lines[0][:50]}{'...' if len(lines[0]) > 50 else ''}",
            "",
            "  Part 1: + and * have equal precedence",
            "  Part 2: + binds tighter than *",
        ],
        "delay": 600,
    }

    part1 = sum(eval_equal_precedence(tokenize(line)) for line in lines)
    part2 = sum(eval_addition_first(tokenize(line)) for line in lines)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (equal precedence)",
            f"  Part 2: {part2} (addition first)",
        ],
        "delay": 500,
    }
