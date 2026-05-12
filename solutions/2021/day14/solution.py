"""
Day 14 - Extended Polymerization
Year: 2021

Simulate polymer pair insertion using pair counting to avoid
exponential string growth.
"""

from collections import Counter


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    sections = puzzle_input.strip().split("\n\n")
    template = sections[0].strip()

    rules = {}
    for line in sections[1].strip().split("\n"):
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    # Count pairs in the template
    pairs = Counter()
    for i in range(len(template) - 1):
        pairs[template[i:i + 2]] += 1

    def step(pairs):
        new_pairs = Counter()
        for pair, count in pairs.items():
            if pair in rules:
                insert = rules[pair]
                new_pairs[pair[0] + insert] += count
                new_pairs[insert + pair[1]] += count
            else:
                new_pairs[pair] += count
        return new_pairs

    def score(pairs):
        # Count each character (each appears in two pairs except first/last)
        counts = Counter()
        for pair, count in pairs.items():
            counts[pair[0]] += count
            counts[pair[1]] += count
        # First and last chars of the original template are only in one pair each
        counts[template[0]] += 1
        counts[template[-1]] += 1
        # Every char is double-counted
        most = max(counts.values()) // 2
        least = min(counts.values()) // 2
        return most - least

    for _ in range(10):
        pairs = step(pairs)
    part1 = score(pairs)

    for _ in range(30):
        pairs = step(pairs)
    part2 = score(pairs)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing polymer growth."""
    sections = puzzle_input.strip().split("\n\n")
    template = sections[0].strip()

    rules = {}
    for line in sections[1].strip().split("\n"):
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    yield {
        "type": "text",
        "lines": [
            "  Extended Polymerization",
            "",
            f"  Template: {template}",
            f"  Rules: {len(rules)}",
        ],
        "delay": 600,
    }

    pairs = Counter()
    for i in range(len(template) - 1):
        pairs[template[i:i + 2]] += 1

    milestones = []
    for s in range(1, 41):
        new_pairs = Counter()
        for pair, count in pairs.items():
            if pair in rules:
                insert = rules[pair]
                new_pairs[pair[0] + insert] += count
                new_pairs[insert + pair[1]] += count
            else:
                new_pairs[pair] += count
        pairs = new_pairs

        if s <= 10 or s % 5 == 0:
            length = sum(pairs.values()) + 1
            milestones.append((s, length))

    lines = ["  Polymer length growth:", ""]
    for s, length in milestones:
        lines.append(f"  Step {s:>2}: {length:>20,} elements")

    yield {
        "type": "text",
        "lines": lines,
        "delay": 800,
    }

    # Compute final scores
    counts = Counter()
    for pair, count in pairs.items():
        counts[pair[0]] += count
        counts[pair[1]] += count
    counts[template[0]] += 1
    counts[template[-1]] += 1
    most = max(counts.values()) // 2
    least = min(counts.values()) // 2

    # Recompute part 1
    pairs10 = Counter()
    for i in range(len(template) - 1):
        pairs10[template[i:i + 2]] += 1
    for _ in range(10):
        new_pairs = Counter()
        for pair, count in pairs10.items():
            if pair in rules:
                insert = rules[pair]
                new_pairs[pair[0] + insert] += count
                new_pairs[insert + pair[1]] += count
            else:
                new_pairs[pair] += count
        pairs10 = new_pairs
    c10 = Counter()
    for pair, count in pairs10.items():
        c10[pair[0]] += count
        c10[pair[1]] += count
    c10[template[0]] += 1
    c10[template[-1]] += 1
    part1 = max(c10.values()) // 2 - min(c10.values()) // 2

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (after 10 steps)",
            f"  Part 2: {most - least} (after 40 steps)",
        ],
        "delay": 500,
    }
