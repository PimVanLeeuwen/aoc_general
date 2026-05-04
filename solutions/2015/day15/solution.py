"""
Day 15 - Science for Hungry People
Year: 2015

Find the optimal cookie recipe by distributing 100 teaspoons across ingredients.
"""

import re
from itertools import product


def parse(puzzle_input):
    ingredients = []
    for line in puzzle_input.strip().split("\n"):
        nums = list(map(int, re.findall(r"-?\d+", line)))
        name = line.split(":")[0]
        ingredients.append((name, nums))
    return ingredients


def distributions(total, n):
    """Generate all ways to split `total` into `n` non-negative integers."""
    if n == 1:
        yield (total,)
        return
    for i in range(total + 1):
        for rest in distributions(total - i, n - 1):
            yield (i,) + rest


def score(ingredients, amounts, calorie_target=None):
    n_props = len(ingredients[0][1])
    totals = []
    for p in range(n_props):
        totals.append(sum(amounts[i] * ingredients[i][1][p] for i in range(len(ingredients))))

    if calorie_target is not None and totals[-1] != calorie_target:
        return 0

    # Multiply all properties except calories, clamping negatives to 0
    result = 1
    for t in totals[:-1]:
        result *= max(0, t)
    return result


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    ingredients = parse(puzzle_input)
    n = len(ingredients)

    best1 = 0
    best2 = 0

    for amounts in distributions(100, n):
        s = score(ingredients, amounts)
        best1 = max(best1, s)

        s500 = score(ingredients, amounts, calorie_target=500)
        best2 = max(best2, s500)

    return str(best1), str(best2)


def visualize(puzzle_input: str):
    """Yield frames showing the recipe optimization search."""
    ingredients = parse(puzzle_input)
    n = len(ingredients)
    names = [ing[0] for ing in ingredients]

    best1_score = 0
    best1_amounts = None
    best2_score = 0
    best2_amounts = None

    improvements = []
    count = 0

    for amounts in distributions(100, n):
        count += 1

        s = score(ingredients, amounts)
        if s > best1_score:
            best1_score = s
            best1_amounts = amounts
            improvements.append(("p1", count, amounts, s))

        s500 = score(ingredients, amounts, calorie_target=500)
        if s500 > best2_score:
            best2_score = s500
            best2_amounts = amounts
            improvements.append(("p2", count, amounts, s500))

    # Show improvements, sampling if there are too many
    step = max(1, len(improvements) // 60)
    shown = improvements[::step]
    if improvements[-1] not in shown:
        shown.append(improvements[-1])

    for part, attempt, amounts, s in shown:
        n_props = len(ingredients[0][1])
        totals = [sum(amounts[i] * ingredients[i][1][p] for i in range(n)) for p in range(n_props)]

        lines = [
            f"  Cookie Optimizer — {count:,} recipes tested",
            "",
            f"  Best {'(all)' if part == 'p1' else '(500 cal)'} so far  (recipe #{attempt:,}):",
            "",
        ]

        for i, name in enumerate(names):
            bar_w = amounts[i] // 2
            bar = "█" * bar_w
            lines.append(f"    {name:>14s}: {amounts[i]:>3d} tsp  {bar}")

        prop_names = ["capacity", "durability", "flavor", "texture", "calories"]
        lines.append("")
        for i, pname in enumerate(prop_names):
            val = totals[i] if i < len(totals) else 0
            marker = "  ← cal" if pname == "calories" else ""
            lines.append(f"    {pname:>10s}: {val:>6d}{marker}")

        lines.append("")
        lines.append(f"  Score: {s:>12,}")

        is_last = (attempt == improvements[-1][1] and part == improvements[-1][0])
        if is_last:
            lines.append("")
            lines.append(f"  ★ Part 1 (best overall):  {best1_score:,}")
            lines.append(f"  ★ Part 2 (500 calories):  {best2_score:,}")

        yield {"type": "text", "lines": lines, "delay": 400 if is_last else 80}