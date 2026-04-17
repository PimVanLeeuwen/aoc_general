"""
Day 21 - Scrambled Letters and Hash
Year: 2016

Apply a sequence of string-scrambling operations forwards (part 1) and find
the input that produces a target scrambled password (part 2).
"""

from itertools import permutations


def apply(s, op):
    w = list(s)
    t = op.split()

    if t[0] == "swap" and t[1] == "position":
        x, y = int(t[2]), int(t[5])
        w[x], w[y] = w[y], w[x]

    elif t[0] == "swap" and t[1] == "letter":
        x, y = t[2], t[5]
        w = [y if c == x else x if c == y else c for c in w]

    elif t[0] == "rotate" and t[1] == "left":
        n = int(t[2]) % len(w)
        w = w[n:] + w[:n]

    elif t[0] == "rotate" and t[1] == "right":
        n = int(t[2]) % len(w)
        w = w[-n:] + w[:-n]

    elif t[0] == "rotate" and t[1] == "based":
        idx = w.index(t[6])
        n = (1 + idx + (1 if idx >= 4 else 0)) % len(w)
        w = w[-n:] + w[:-n]

    elif t[0] == "reverse":
        x, y = int(t[2]), int(t[4])
        w[x:y + 1] = w[x:y + 1][::-1]

    elif t[0] == "move":
        x, y = int(t[2]), int(t[5])
        ch = w.pop(x)
        w.insert(y, ch)

    return "".join(w)


def scramble(password, ops):
    for op in ops:
        password = apply(password, op)
    return password


def solve(puzzle_input: str) -> tuple[str, str]:
    ops = puzzle_input.strip().splitlines()

    part1 = scramble("abcdefgh", ops)

    # Part 2: find input that scrambles to "fbgdceah"
    # 8! = 40320 — brute-force all permutations is fast enough
    target = "fbgdceah"
    part2 = next(
        "".join(p) for p in permutations("abcdefgh")
        if scramble("".join(p), ops) == target
    )

    return part1, part2


def visualize(puzzle_input: str):
    """Show each scrambling operation applied step by step to 'abcdefgh'."""
    ops = puzzle_input.strip().splitlines()
    password = "abcdefgh"

    yield {
        "type": "text",
        "lines": [
            "  Scrambling: abcdefgh",
            "",
            f"  Start: {password}",
        ],
        "delay": 400,
    }

    for i, op in enumerate(ops):
        before = password
        password = apply(password, op)

        # Highlight which positions changed
        diff = "".join(
            "^" if a != b else " " for a, b in zip(before, password)
        )

        yield {
            "type": "text",
            "lines": [
                f"  Step {i + 1:>3} / {len(ops)}",
                "",
                f"  Op:     {op}",
                f"  Before: {before}",
                f"  After:  {password}",
                f"          {diff}",
            ],
            "delay": 200,
        }

    yield {
        "type": "text",
        "lines": [
            f"  Done — {len(ops)} operations applied.",
            "",
            f"  Scrambled: {password}",
        ],
        "delay": 800,
    }
