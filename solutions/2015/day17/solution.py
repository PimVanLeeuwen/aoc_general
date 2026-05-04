"""
Day 17 - No Such Thing as Too Much
Year: 2015

Count combinations of containers that exactly fit 150 liters of eggnog.
"""

from itertools import combinations


def find_combos(containers, target):
    """Find all subsets of containers that sum to target."""
    valid = []
    for r in range(1, len(containers) + 1):
        for combo in combinations(enumerate(containers), r):
            if sum(c for _, c in combo) == target:
                valid.append(combo)
    return valid


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    containers = [int(x) for x in puzzle_input.strip().split("\n")]
    target = 150

    valid = find_combos(containers, target)

    part1 = len(valid)

    min_containers = min(len(combo) for combo in valid)
    part2 = sum(1 for combo in valid if len(combo) == min_containers)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the combination search by container count."""
    containers = [int(x) for x in puzzle_input.strip().split("\n")]
    target = 150
    n = len(containers)

    counts_by_size = {}
    total_found = 0

    for r in range(1, n + 1):
        found = 0
        for combo in combinations(containers, r):
            if sum(combo) == target:
                found += 1
        if found > 0:
            counts_by_size[r] = found
            total_found += found

        lines = [
            f"  Eggnog Container Combinations",
            f"  Target: {target} liters | {n} containers available",
            "",
            f"  Testing subsets of size {r} / {n}...",
            "",
            f"  Size  |  Valid combinations",
            f"  ------+---------------------",
        ]

        max_count = max(counts_by_size.values()) if counts_by_size else 1
        for size in sorted(counts_by_size.keys()):
            count = counts_by_size[size]
            bar_w = round(count / max_count * 30)
            bar = "█" * bar_w
            lines.append(f"    {size:>2d}   |  {count:>4d}  {bar}")

        lines.append("")
        lines.append(f"  Total valid: {total_found}")

        if r == n:
            min_size = min(counts_by_size.keys())
            lines.append("")
            lines.append(f"  ★ Part 1: {total_found} combinations")
            lines.append(f"  ★ Part 2: {counts_by_size[min_size]} (using minimum {min_size} containers)")

        yield {"type": "text", "lines": lines, "delay": 500 if r == n else 150}
