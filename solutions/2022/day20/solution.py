"""
Day 20 - Grove Positioning System
Year: 2022

Mix a circular list of numbers by moving each element
by its value, then find grove coordinates.
"""


def mix(numbers, times=1):
    """Mix the list the given number of times. Return the mixed list."""
    n = len(numbers)
    indices = list(range(n))

    for _ in range(times):
        for original_idx in range(n):
            current_pos = indices.index(original_idx)
            indices.pop(current_pos)
            new_pos = (current_pos + numbers[original_idx]) % (n - 1)
            indices.insert(new_pos, original_idx)

    return [numbers[i] for i in indices]


def grove_coords(mixed):
    """Sum values at positions 1000, 2000, 3000 after zero."""
    zero_pos = mixed.index(0)
    n = len(mixed)
    return sum(mixed[(zero_pos + offset) % n] for offset in [1000, 2000, 3000])


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    numbers = list(map(int, puzzle_input.strip().split("\n")))

    # Part 1: mix once
    mixed1 = mix(numbers, times=1)
    part1 = grove_coords(mixed1)

    # Part 2: multiply by decryption key, mix 10 times
    key = 811589153
    scaled = [x * key for x in numbers]
    mixed2 = mix(scaled, times=10)
    part2 = grove_coords(mixed2)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing mixing process."""
    numbers = list(map(int, puzzle_input.strip().split("\n")))

    yield {
        "type": "text",
        "lines": [
            "  Grove Positioning System",
            "",
            f"  Numbers to mix: {len(numbers)}",
            f"  First few: {numbers[:5]}...",
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
            f"  Part 1: {part1} (single mix)",
            f"  Part 2: {part2} (10x mix with key)",
        ],
        "delay": 500,
    }
