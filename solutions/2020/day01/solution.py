"""
Day 1 - Report Repair
Year: 2020

Find pairs and triples of numbers that sum to 2020, then multiply them.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    numbers = set(int(x) for x in puzzle_input.strip().split("\n"))

    # Part 1: find two numbers summing to 2020
    part1 = 0
    for n in numbers:
        if 2020 - n in numbers:
            part1 = n * (2020 - n)
            break

    # Part 2: find three numbers summing to 2020
    part2 = 0
    nums_list = list(numbers)
    for i, a in enumerate(nums_list):
        for b in nums_list[i + 1:]:
            c = 2020 - a - b
            if c in numbers and c != a and c != b:
                part2 = a * b * c
                break
        if part2:
            break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the expense report search."""
    numbers = sorted(int(x) for x in puzzle_input.strip().split("\n"))
    num_set = set(numbers)

    yield {
        "type": "text",
        "lines": [
            "  Report Repair",
            "",
            f"  Expense entries: {len(numbers)}",
            f"  Range: {numbers[0]} - {numbers[-1]}",
            "",
            "  Finding pairs and triples summing to 2020...",
        ],
        "delay": 600,
    }

    # Find pair
    for n in numbers:
        if 2020 - n in num_set:
            a, b = n, 2020 - n
            break

    # Find triple
    p2a = p2b = p2c = 0
    for i, x in enumerate(numbers):
        for y in numbers[i + 1:]:
            z = 2020 - x - y
            if z in num_set:
                p2a, p2b, p2c = x, y, z
                break
        if p2a:
            break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Pair: {a} + {b} = 2020",
            f"  Part 1: {a * b}",
            "",
            f"  Triple: {p2a} + {p2b} + {p2c} = 2020",
            f"  Part 2: {p2a * p2b * p2c}",
        ],
        "delay": 500,
    }
