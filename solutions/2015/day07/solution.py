"""
Day 07 - Some Assembly Required
Year: 2015

Simulate a circuit of 16-bit wires connected by logic gates.
Evaluate wire 'a'; then override wire 'b' with that value and re-evaluate.
"""


def parse(puzzle_input: str) -> dict[str, str]:
    """Return a mapping of wire name → raw instruction RHS."""
    rules = {}
    for line in puzzle_input.strip().split("\n"):
        src, dst = line.split(" -> ")
        rules[dst.strip()] = src.strip()
    return rules


def evaluate(wire: str, rules: dict, cache: dict) -> int:
    if wire in cache:
        return cache[wire]

    # Literal integer
    if wire.lstrip("-").isdigit():
        return int(wire)

    expr = rules[wire]
    parts = expr.split()

    if len(parts) == 1:
        result = evaluate(parts[0], rules, cache)
    elif len(parts) == 2:              # NOT x
        result = (~evaluate(parts[1], rules, cache)) & 0xFFFF
    elif parts[1] == "AND":
        result = evaluate(parts[0], rules, cache) & evaluate(parts[2], rules, cache)
    elif parts[1] == "OR":
        result = evaluate(parts[0], rules, cache) | evaluate(parts[2], rules, cache)
    elif parts[1] == "LSHIFT":
        result = (evaluate(parts[0], rules, cache) << int(parts[2])) & 0xFFFF
    elif parts[1] == "RSHIFT":
        result = evaluate(parts[0], rules, cache) >> int(parts[2])
    else:
        raise ValueError(f"Unknown expression: {expr}")

    cache[wire] = result
    return result


def solve(puzzle_input: str) -> tuple[str, str]:
    rules = parse(puzzle_input)

    part1 = evaluate("a", rules, {})

    # Part 2: override wire b with the part 1 answer, re-evaluate a
    rules["b"] = str(part1)
    part2 = evaluate("a", rules, {})

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Show each wire being resolved in dependency order."""
    rules = parse(puzzle_input)
    cache: dict[str, int] = {}
    resolved_order: list[tuple[str, int]] = []

    # Force full evaluation by resolving 'a', which pulls in all dependencies
    def evaluate_tracked(wire: str) -> int:
        if wire in cache:
            return cache[wire]
        if wire.lstrip("-").isdigit():
            return int(wire)
        expr = rules[wire]
        parts = expr.split()
        if len(parts) == 1:
            result = evaluate_tracked(parts[0])
        elif len(parts) == 2:
            result = (~evaluate_tracked(parts[1])) & 0xFFFF
        elif parts[1] == "AND":
            result = evaluate_tracked(parts[0]) & evaluate_tracked(parts[2])
        elif parts[1] == "OR":
            result = evaluate_tracked(parts[0]) | evaluate_tracked(parts[2])
        elif parts[1] == "LSHIFT":
            result = (evaluate_tracked(parts[0]) << int(parts[2])) & 0xFFFF
        else:  # RSHIFT
            result = evaluate_tracked(parts[0]) >> int(parts[2])
        cache[wire] = result
        resolved_order.append((wire, result))
        return result

    evaluate_tracked("a")

    # Emit one frame per resolved wire, sampling to ~200 frames
    total = len(resolved_order)
    step = max(1, total // 200)

    for i in range(0, total, step):
        wire, value = resolved_order[i]
        expr = rules.get(wire, str(value))

        # Show last 10 resolved wires
        recent = resolved_order[max(0, i - 9):i + 1]
        lines = [
            f"Resolving circuit... ({i + 1}/{total} wires)",
            "",
            "  Recent resolutions:",
        ]
        for w, v in recent:
            marker = ">>>" if w == wire else "   "
            lines.append(f"  {marker} {w:>4} = {v:>5}  ({rules.get(w, str(v))})")

        lines += ["", f"  Total resolved: {i + 1}"]
        if i + 1 == total:
            lines.append(f"  Wire 'a' = {cache['a']}")

        yield {"type": "text", "lines": lines, "delay": 60}
