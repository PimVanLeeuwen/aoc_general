"""
Day 13 - Knights of the Dinner Table
Year: 2015

Find the optimal circular seating arrangement to maximize total happiness.
"""

from itertools import permutations
from collections import defaultdict


def parse(puzzle_input):
    happiness = defaultdict(dict)
    people = set()
    for line in puzzle_input.strip().split("\n"):
        parts = line.rstrip(".").split()
        person = parts[0]
        sign = 1 if parts[2] == "gain" else -1
        amount = sign * int(parts[3])
        neighbor = parts[-1]
        happiness[person][neighbor] = amount
        people.add(person)
    return happiness, sorted(people)


def total_happiness(arrangement, happiness):
    n = len(arrangement)
    return sum(
        happiness[arrangement[i]][arrangement[(i + 1) % n]]
        + happiness[arrangement[(i + 1) % n]][arrangement[i]]
        for i in range(n)
    )


def best_happiness(happiness, people):
    # Fix first person to avoid equivalent rotations
    first = people[0]
    rest = people[1:]
    return max(
        total_happiness((first,) + perm, happiness)
        for perm in permutations(rest)
    )


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    happiness, people = parse(puzzle_input)

    part1 = best_happiness(happiness, people)

    # Part 2: add yourself with 0 happiness toward/from everyone
    for person in people:
        happiness["Me"][person] = 0
        happiness[person]["Me"] = 0
    people_with_me = people + ["Me"]

    part2 = best_happiness(happiness, people_with_me)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the search for optimal seating."""
    happiness, people = parse(puzzle_input)

    import math

    def arrangement_display(arr, h):
        """Render a circular table as text."""
        n = len(arr)
        total = total_happiness(arr, h)
        lines = [f"  Total happiness: {total:>+4d}", ""]

        # Show each pair around the table
        for i in range(n):
            a = arr[i]
            b = arr[(i + 1) % n]
            h_ab = h[a][b]
            h_ba = h[b][a]
            lines.append(f"    {a:>8s} ←{h_ba:>+4d} / {h_ab:>+4d}→ {b}")

        return lines, total

    # Part 1: collect best arrangements as we search
    first = people[0]
    rest = people[1:]

    best_score = float("-inf")
    best_arr = None
    samples = []
    count = 0

    for perm in permutations(rest):
        arr = (first,) + perm
        score = total_happiness(arr, happiness)
        count += 1
        if score > best_score:
            best_score = score
            best_arr = arr
            samples.append((arr, score, count))

    # Show the progression of best-found arrangements
    for arr, score, attempt in samples:
        display, _ = arrangement_display(arr, happiness)
        lines = [
            f"  Part 1: Searching {len(people)} guests ({count:,} arrangements)",
            f"  Best so far (attempt #{attempt:,}):",
            "",
        ] + display

        yield {"type": "text", "lines": lines, "delay": 200}

    # Final Part 1
    display, _ = arrangement_display(best_arr, happiness)
    lines = [
        f"  ★ Part 1 — Optimal arrangement found!",
        "",
    ] + display
    yield {"type": "text", "lines": lines, "delay": 600}

    # Part 2: add "Me"
    for person in people:
        happiness["Me"][person] = 0
        happiness[person]["Me"] = 0
    people_with_me = people + ["Me"]

    rest2 = people_with_me[1:]
    best_score2 = float("-inf")
    best_arr2 = None
    samples2 = []
    count2 = 0

    for perm in permutations(rest2):
        arr = (people_with_me[0],) + perm
        score = total_happiness(arr, happiness)
        count2 += 1
        if score > best_score2:
            best_score2 = score
            best_arr2 = arr
            samples2.append((arr, score, count2))

    # Show a subset of improvements for Part 2
    step = max(1, len(samples2) // 8)
    for i in range(0, len(samples2), step):
        arr, score, attempt = samples2[i]
        display, _ = arrangement_display(arr, happiness)
        lines = [
            f"  Part 2: Adding \"Me\" — {len(people_with_me)} guests ({count2:,} arrangements)",
            f"  Best so far (attempt #{attempt:,}):",
            "",
        ] + display

        yield {"type": "text", "lines": lines, "delay": 200}

    # Final Part 2
    display, _ = arrangement_display(best_arr2, happiness)
    lines = [
        f"  ★ Part 2 — Optimal arrangement with Me!",
        "",
    ] + display
    yield {"type": "text", "lines": lines, "delay": 600}