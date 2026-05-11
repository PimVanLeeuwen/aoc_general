"""
Day 24 - It Hangs in the Balance
Year: 2015

Split packages into equal-weight groups, minimizing the size (then quantum
entanglement) of the first group.
"""

from itertools import combinations
from math import prod


def find_min_qe(weights, num_groups):
    """Find the minimum QE for the smallest possible first group."""
    target = sum(weights) // num_groups

    for size in range(1, len(weights)):
        qes = []
        for combo in combinations(weights, size):
            if sum(combo) == target:
                qes.append(prod(combo))
        if qes:
            return min(qes)

    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    weights = [int(x) for x in puzzle_input.strip().splitlines()]

    part1 = find_min_qe(weights, 3)
    part2 = find_min_qe(weights, 4)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the search for optimal groupings."""
    weights = [int(x) for x in puzzle_input.strip().splitlines()]

    for num_groups, label in [(3, "Part 1 (3 groups)"), (4, "Part 2 (4 groups)")]:
        target = sum(weights) // num_groups

        yield {
            "type": "text",
            "lines": [
                f"  === {label} ===",
                "",
                f"  Packages: {len(weights)}",
                f"  Total weight: {sum(weights)}",
                f"  Target per group: {target}",
                "",
                "  Searching for smallest first group...",
            ],
            "delay": 600,
        }

        found = False
        for size in range(1, len(weights)):
            valid = []
            checked = 0
            for combo in combinations(weights, size):
                checked += 1
                if sum(combo) == target:
                    valid.append((prod(combo), combo))

            if valid:
                valid.sort()
                best_qe, best_combo = valid[0]

                lines = [
                    f"  === {label} ===",
                    "",
                    f"  Group size {size}: found {len(valid)} valid combination(s)",
                    f"  Checked {checked:,} combinations of size {size}",
                    "",
                    f"  Best group: {list(best_combo)}",
                    f"  Weight: {sum(best_combo)}",
                    f"  QE: {' x '.join(str(w) for w in best_combo)} = {best_qe:,}",
                ]

                if len(valid) > 1:
                    lines.append("")
                    lines.append(f"  Runner-up QEs: {', '.join(f'{qe:,}' for qe, _ in valid[1:min(4, len(valid))])}")

                yield {"type": "text", "lines": lines, "delay": 600}
                found = True
                break
            else:
                yield {
                    "type": "text",
                    "lines": [
                        f"  === {label} ===",
                        "",
                        f"  Group size {size}: no valid combinations",
                        f"  Checked {checked:,} combinations",
                        "  Trying larger group...",
                    ],
                    "delay": 200,
                }

        if found:
            yield {
                "type": "text",
                "lines": [
                    f"  === {label} — Result ===",
                    "",
                    f"  Minimum group size: {len(best_combo)}",
                    f"  Quantum entanglement: {best_qe:,}",
                ],
                "delay": 800,
            }