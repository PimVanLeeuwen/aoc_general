"""
Day 19 - An Elephant Named Joseph
Year: 2016

Two variants of the Josephus problem: elves stealing from the left (every
second elf eliminated) and from directly across the circle.
"""


def josephus_left(n):
    """Elf that wins when each elf steals from the one to their left.

    Classic Josephus with k=2. If n = 2^m + L, the winner is 2*L + 1.
    """
    # Highest power of 2 <= n
    p = 1
    while p * 2 <= n:
        p *= 2
    return 2 * (n - p) + 1


def josephus_across(n):
    """Elf that wins when each elf steals from directly across the circle.

    The winner follows a base-3 pattern:
      - n == 3^m          → winner = n
      - 3^m < n <= 2*3^m  → winner = n - 3^m
      - 2*3^m < n         → winner = 2*n - 3^(m+1)
    """
    p = 1
    while p * 3 <= n:
        p *= 3
    if n == p:
        return n
    if n <= 2 * p:
        return n - p
    return 2 * n - 3 * p


def solve(puzzle_input: str) -> tuple[str, str]:
    n = int(puzzle_input.strip())
    return str(josephus_left(n)), str(josephus_across(n))


def visualize(puzzle_input: str):
    """Simulate both games with a small circle, showing each elimination step."""
    from collections import deque

    demo_n = min(int(puzzle_input.strip()), 20)

    # ── Part 1 simulation ─────────────────────────────────────────────────────
    circle = deque(range(1, demo_n + 1))
    step = 0
    while len(circle) > 1:
        step += 1
        active = list(circle)
        thief = circle[0]
        victim = circle[1]

        yield {
            "type": "text",
            "lines": [
                f"  Part 1 — steal from left  (n={demo_n})",
                "",
                f"  Circle: {' '.join(str(e) for e in active)}",
                f"  Step {step}: Elf {thief} takes from Elf {victim}",
                f"  Elf {victim} is removed.",
            ],
            "delay": 300,
        }
        circle.rotate(-1)   # advance past the thief
        circle.popleft()    # remove victim (now at front)

    yield {
        "type": "text",
        "lines": [
            f"  Part 1 — steal from left  (n={demo_n})",
            "",
            f"  Winner: Elf {circle[0]}",
            f"  Formula result: {josephus_left(demo_n)}",
        ],
        "delay": 600,
    }

    # ── Part 2 simulation ─────────────────────────────────────────────────────
    # Simple list simulation: current elf is at index i, steals from index
    # (i + len//2) % len, then advance i to the next elf.
    elves2 = list(range(1, demo_n + 1))
    idx = 0
    step = 0
    while len(elves2) > 1:
        step += 1
        thief = elves2[idx]
        across = (idx + len(elves2) // 2) % len(elves2)
        victim = elves2[across]

        yield {
            "type": "text",
            "lines": [
                f"  Part 2 — steal from across  (n={demo_n})",
                "",
                f"  Circle: {' '.join(str(e) for e in elves2)}",
                f"  Step {step}: Elf {thief} takes from Elf {victim}",
                f"  Elf {victim} is removed.",
            ],
            "delay": 300,
        }

        elves2.pop(across)
        if across > idx:
            idx = (idx + 1) % len(elves2)
        else:
            idx = idx % len(elves2)

    winner2 = elves2[0]
    yield {
        "type": "text",
        "lines": [
            f"  Part 2 — steal from across  (n={demo_n})",
            "",
            f"  Winner: Elf {winner2}",
            f"  Formula result: {josephus_across(demo_n)}",
            "",
            f"  Actual input (n={int(puzzle_input.strip())}):",
            f"  Part 1 winner: {josephus_left(int(puzzle_input.strip()))}",
            f"  Part 2 winner: {josephus_across(int(puzzle_input.strip()))}",
        ],
        "delay": 800,
    }
