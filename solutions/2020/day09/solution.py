"""
Day 9 - Encoding Error
Year: 2020

Find the first number in a sequence that isn't the sum of two of the
preceding 25 numbers, then find a contiguous range that sums to it.
"""


def find_invalid(numbers, preamble=25):
    """Find the first number not expressible as a sum of two in the preceding window."""
    for i in range(preamble, len(numbers)):
        target = numbers[i]
        window = set(numbers[i - preamble:i])
        if not any(target - n in window and target - n != n for n in window):
            return target
    return -1


def find_contiguous_sum(numbers, target):
    """Find a contiguous range summing to target using a sliding window."""
    left = 0
    current_sum = 0
    for right in range(len(numbers)):
        current_sum += numbers[right]
        while current_sum > target and left < right:
            current_sum -= numbers[left]
            left += 1
        if current_sum == target and right > left:
            window = numbers[left:right + 1]
            return min(window) + max(window)
    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    numbers = [int(x) for x in puzzle_input.strip().split("\n")]

    part1 = find_invalid(numbers)
    part2 = find_contiguous_sum(numbers, part1)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the XMAS cipher analysis."""
    numbers = [int(x) for x in puzzle_input.strip().split("\n")]

    invalid = find_invalid(numbers)
    invalid_idx = numbers.index(invalid)

    yield {
        "type": "text",
        "lines": [
            "  Encoding Error — XMAS Cipher",
            "",
            f"  Sequence length: {len(numbers)}",
            f"  Preamble: 25 numbers",
            f"  Range: {min(numbers):,} - {max(numbers):,}",
        ],
        "delay": 600,
    }

    # Find the contiguous range for display
    left = 0
    current_sum = 0
    for right in range(len(numbers)):
        current_sum += numbers[right]
        while current_sum > invalid and left < right:
            current_sum -= numbers[left]
            left += 1
        if current_sum == invalid and right > left:
            window = numbers[left:right + 1]
            weakness = min(window) + max(window)
            break

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {invalid} (at index {invalid_idx})",
            f"  Part 2: {weakness} (range [{left}:{right + 1}],",
            f"          {right - left + 1} numbers, min+max)",
        ],
        "delay": 500,
    }
