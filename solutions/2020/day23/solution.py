"""
Day 23 - Crab Cups
Year: 2020

Simulate a cup circle game using a linked-list array for O(1) operations,
first with 9 cups for 100 moves, then with 1 million cups for 10 million moves.
"""


def play_cups(labels, num_cups, num_moves):
    """Simulate the cup game using an array-based linked list.

    next_cup[i] stores the label of the cup clockwise from cup i.
    This gives O(1) removal, insertion, and destination lookup.
    """
    # Build the linked list
    next_cup = [0] * (num_cups + 1)

    # Link the initial cups
    for i in range(len(labels) - 1):
        next_cup[labels[i]] = labels[i + 1]

    # If extending beyond original labels, link to the extra cups
    if num_cups > len(labels):
        next_cup[labels[-1]] = len(labels) + 1
        for i in range(len(labels) + 1, num_cups):
            next_cup[i] = i + 1
        next_cup[num_cups] = labels[0]
    else:
        next_cup[labels[-1]] = labels[0]

    current = labels[0]

    for _ in range(num_moves):
        # Pick up three cups after current
        a = next_cup[current]
        b = next_cup[a]
        c = next_cup[b]

        # Remove them from the circle
        next_cup[current] = next_cup[c]

        # Find destination
        dest = current - 1 if current > 1 else num_cups
        while dest == a or dest == b or dest == c:
            dest = dest - 1 if dest > 1 else num_cups

        # Insert the three cups after destination
        next_cup[c] = next_cup[dest]
        next_cup[dest] = a

        current = next_cup[current]

    return next_cup


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    labels = [int(c) for c in puzzle_input.strip()]

    # Part 1: 9 cups, 100 moves
    next_cup = play_cups(labels, 9, 100)
    result = []
    cup = next_cup[1]
    while cup != 1:
        result.append(str(cup))
        cup = next_cup[cup]
    part1 = "".join(result)

    # Part 2: 1 million cups, 10 million moves
    next_cup = play_cups(labels, 1_000_000, 10_000_000)
    a = next_cup[1]
    b = next_cup[a]
    part2 = a * b

    return part1, str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the cup game progression."""
    labels = [int(c) for c in puzzle_input.strip()]

    yield {
        "type": "text",
        "lines": [
            "  Crab Cups",
            "",
            f"  Starting arrangement: {''.join(str(c) for c in labels)}",
        ],
        "delay": 600,
    }

    # Show first few moves of part 1
    next_cup = [0] * 10
    for i in range(len(labels) - 1):
        next_cup[labels[i]] = labels[i + 1]
    next_cup[labels[-1]] = labels[0]

    current = labels[0]
    frames = []

    for move in range(min(20, 100)):
        a = next_cup[current]
        b = next_cup[a]
        c = next_cup[b]
        next_cup[current] = next_cup[c]

        dest = current - 1 if current > 1 else 9
        while dest == a or dest == b or dest == c:
            dest = dest - 1 if dest > 1 else 9

        next_cup[c] = next_cup[dest]
        next_cup[dest] = a

        current = next_cup[current]

        # Build circle string
        circle = []
        cup = current
        for _ in range(9):
            circle.append(str(cup))
            cup = next_cup[cup]

        frames.append(f"  Move {move + 1:>3}: [{circle[0]}] {' '.join(circle[1:])}")

    yield {
        "type": "text",
        "lines": ["  First 20 moves:", ""] + frames,
        "delay": 800,
    }

    # Full results
    next_cup_p1 = play_cups(labels, 9, 100)
    result = []
    cup = next_cup_p1[1]
    while cup != 1:
        result.append(str(cup))
        cup = next_cup_p1[cup]
    part1 = "".join(result)

    next_cup_p2 = play_cups(labels, 1_000_000, 10_000_000)
    a = next_cup_p2[1]
    b = next_cup_p2[a]
    part2 = a * b

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (labels after cup 1)",
            f"  Part 2: {part2} (product of two cups after 1)",
            f"    Cup A: {a}",
            f"    Cup B: {b}",
        ],
        "delay": 500,
    }
