"""
Day 03 - Binary Diagnostic
Year: 2021

Analyze binary diagnostic numbers to find power consumption and
life support rating through bit-frequency filtering.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")
    width = len(lines[0])

    # Part 1: gamma and epsilon from most/least common bits
    gamma = 0
    epsilon = 0
    for bit in range(width):
        ones = sum(1 for line in lines if line[bit] == "1")
        zeros = len(lines) - ones
        if ones >= zeros:
            gamma |= 1 << (width - 1 - bit)
        else:
            epsilon |= 1 << (width - 1 - bit)
    part1 = gamma * epsilon

    # Part 2: oxygen generator and CO2 scrubber ratings
    def filter_by_bit_criteria(numbers, keep_most_common):
        remaining = list(numbers)
        for bit in range(width):
            if len(remaining) == 1:
                break
            ones = sum(1 for n in remaining if n[bit] == "1")
            zeros = len(remaining) - ones
            if keep_most_common:
                keep = "1" if ones >= zeros else "0"
            else:
                keep = "0" if ones >= zeros else "1"
            remaining = [n for n in remaining if n[bit] == keep]
        return int(remaining[0], 2)

    oxygen = filter_by_bit_criteria(lines, keep_most_common=True)
    co2 = filter_by_bit_criteria(lines, keep_most_common=False)
    part2 = oxygen * co2

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing binary diagnostic filtering."""
    lines = puzzle_input.strip().split("\n")
    width = len(lines[0])

    yield {
        "type": "text",
        "lines": [
            "  Binary Diagnostic",
            "",
            f"  Numbers: {len(lines)}",
            f"  Bit width: {width}",
        ],
        "delay": 600,
    }

    # Show oxygen filtering steps
    remaining = list(lines)
    filter_lines = ["  Oxygen generator filtering:", ""]
    for bit in range(width):
        if len(remaining) == 1:
            break
        ones = sum(1 for n in remaining if n[bit] == "1")
        zeros = len(remaining) - ones
        keep = "1" if ones >= zeros else "0"
        remaining = [n for n in remaining if n[bit] == keep]
        filter_lines.append(f"  Bit {bit}: keep '{keep}' -> {len(remaining)} remaining")
    oxygen = int(remaining[0], 2)
    filter_lines.append(f"  Oxygen: {remaining[0]} = {oxygen}")

    yield {
        "type": "text",
        "lines": filter_lines,
        "delay": 800,
    }

    # Compute results
    gamma = 0
    for bit in range(width):
        ones = sum(1 for line in lines if line[bit] == "1")
        if ones >= len(lines) - ones:
            gamma |= 1 << (width - 1 - bit)
    epsilon = gamma ^ ((1 << width) - 1)

    remaining = list(lines)
    for bit in range(width):
        if len(remaining) == 1:
            break
        ones = sum(1 for n in remaining if n[bit] == "1")
        keep = "0" if ones >= len(remaining) - ones else "1"
        remaining = [n for n in remaining if n[bit] == keep]
    co2 = int(remaining[0], 2)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {gamma * epsilon}",
            f"    Gamma: {gamma}, Epsilon: {epsilon}",
            "",
            f"  Part 2: {oxygen * co2}",
            f"    Oxygen: {oxygen}, CO2: {co2}",
        ],
        "delay": 500,
    }
