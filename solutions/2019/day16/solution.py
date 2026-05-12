"""
Day 16 - Flawed Frequency Transmission
Year: 2019

Apply a pattern-based FFT algorithm for 100 phases. Part 2 exploits
the structure when the offset is in the second half of the signal.
"""

BASE_PATTERN = [0, 1, 0, -1]


def fft_phase(digits):
    """Apply one FFT phase to the digit list."""
    n = len(digits)
    result = []
    for i in range(n):
        total = 0
        for j in range(i, n):
            p = BASE_PATTERN[((j + 1) // (i + 1)) % 4]
            if p:
                total += digits[j] * p
        result.append(abs(total) % 10)
    return result


def fft_part1(digits, phases=100):
    """Run FFT for given number of phases, return first 8 digits as string."""
    for _ in range(phases):
        digits = fft_phase(digits)
    return "".join(str(d) for d in digits[:8])


def fft_part2(digits_str, phases=100):
    """Part 2: signal repeated 10000x, offset from first 7 digits.

    When offset >= len/2, pattern for position i is all zeros up to i,
    then all ones. So output[i] = sum(input[i:]) mod 10.
    Compute from the back: suffix sums, applied 100 times.
    """
    offset = int(digits_str[:7])
    total_len = len(digits_str) * 10000

    # Only need digits from offset to end
    relevant = []
    for i in range(offset, total_len):
        relevant.append(int(digits_str[i % len(digits_str)]))

    for _ in range(phases):
        # Compute suffix sums from right to left
        suffix = 0
        for i in range(len(relevant) - 1, -1, -1):
            suffix += relevant[i]
            relevant[i] = suffix % 10

    return "".join(str(d) for d in relevant[:8])


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    digits_str = puzzle_input.strip()
    digits = [int(c) for c in digits_str]

    part1 = fft_part1(digits)
    part2 = fft_part2(digits_str)

    return part1, part2


def visualize(puzzle_input: str):
    """Yield frames showing the FFT process."""
    digits_str = puzzle_input.strip()
    digits = [int(c) for c in digits_str]

    yield {
        "type": "text",
        "lines": [
            "  Flawed Frequency Transmission",
            "",
            f"  Input signal: {len(digits)} digits",
            f"  First 20: {digits_str[:20]}...",
        ],
        "delay": 600,
    }

    # Part 1: show phase progression
    current = list(digits)
    for phase in range(1, 101):
        current = fft_phase(current)
        if phase in (1, 2, 5, 10, 25, 50, 100):
            first8 = "".join(str(d) for d in current[:8])
            yield {
                "type": "text",
                "lines": [
                    f"  Part 1: Phase {phase}/100",
                    "",
                    f"  First 8 digits: {first8}",
                    f"  First 30: {''.join(str(d) for d in current[:30])}...",
                ],
                "delay": 200 if phase < 50 else 400,
            }

    part1 = "".join(str(d) for d in current[:8])

    # Part 2
    offset = int(digits_str[:7])
    total_len = len(digits_str) * 10000

    yield {
        "type": "text",
        "lines": [
            "  Part 2: 10000x repeated signal",
            "",
            f"  Total length: {total_len:,} digits",
            f"  Message offset: {offset:,}",
            f"  Relevant suffix: {total_len - offset:,} digits",
            "",
            "  Computing suffix sums for 100 phases...",
        ],
        "delay": 600,
    }

    part2 = fft_part2(digits_str)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1}",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
