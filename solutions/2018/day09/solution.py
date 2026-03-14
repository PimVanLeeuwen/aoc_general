"""
Day 09 - Marble Mania
Year: 2018

Simulate a marble circle game using a deque; find the highest score.
"""
import re
from collections import deque


def play(num_players: int, last_marble: int) -> int:
    scores = [0] * num_players
    circle = deque([0])
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % num_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return max(scores)


def solve(puzzle_input: str) -> tuple[str, str]:
    nums = list(map(int, re.findall(r'\d+', puzzle_input)))
    num_players, last_marble = nums[0], nums[1]
    part1 = play(num_players, last_marble)
    part2 = play(num_players, last_marble * 100)
    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    nums = list(map(int, re.findall(r'\d+', puzzle_input)))
    num_players, last_marble = nums[0], nums[1]

    # ── Animate early turns with the actual circle ─────────────────────────────
    SHOW_TURNS = 80  # animate first N marbles showing the full circle

    scores = [0] * num_players
    circle = deque([0])

    yield {
        "type": "text",
        "lines": [
            "Marble Mania",
            "",
            f"Players      : {num_players}",
            f"Last marble  : {last_marble:,}  (Part 1)",
            f"             : {last_marble * 100:,}  (Part 2)",
            "",
            "Simulating...",
            "",
            "Circle: (0)",
        ],
        "delay": 800,
    }

    for marble in range(1, last_marble + 1):
        is_special = marble % 23 == 0
        player = marble % num_players

        if is_special:
            circle.rotate(7)
            removed = circle.pop()
            scores[player] += marble + removed
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

        if marble <= SHOW_TURNS:
            # Render circle with current marble highlighted
            lst = list(circle)
            current = lst[-1]
            parts = []
            for m in lst:
                parts.append(f"({m})" if m == current else str(m))
            circle_str = "  ".join(parts)

            lines = [
                f"Turn {marble:>3}  —  Player {player + 1}",
                "",
            ]
            if is_special:
                lines += [
                    f"  Marble {marble} is a multiple of 23!",
                    f"  Kept marble {marble}, removed marble {removed}",
                    f"  Player {player + 1} scores {marble + removed}",
                    "",
                ]
            lines += [
                "Circle:",
                circle_str[:120] + ("…" if len(circle_str) > 120 else ""),
                "",
                f"High score so far: {max(scores):,}",
            ]
            yield {"type": "text", "lines": lines, "delay": 120}

        elif marble % max(1, last_marble // 40) == 0 or marble == last_marble:
            pct = marble * 100 // last_marble
            bar = "█" * (pct // 2) + "░" * (50 - pct // 2)
            yield {
                "type": "text",
                "lines": [
                    "Part 1 — Simulating marble game",
                    "",
                    f"  Progress : {marble:,} / {last_marble:,}  ({pct}%)",
                    f"  [{bar}]",
                    "",
                    f"  High score so far: {max(scores):,}",
                    f"  Players           : {num_players}",
                ],
                "delay": 80,
            }

    part1 = max(scores)

    yield {
        "type": "text",
        "lines": [
            "Part 1 — Complete!",
            "",
            f"Marbles played : {last_marble:,}",
            f"Players        : {num_players}",
            f"Winning score  : {part1:,}",
            "",
            f"Answer: {part1}",
        ],
        "delay": 1200,
    }

    # ── Part 2: run full game with 100× marbles, show progress bar ────────────
    last_marble_2 = last_marble * 100
    scores2 = [0] * num_players
    circle2 = deque([0])

    for marble in range(1, last_marble_2 + 1):
        if marble % 23 == 0:
            circle2.rotate(7)
            circle2.pop()
            scores2[marble % num_players] += marble
            circle2.rotate(-1)
        else:
            circle2.rotate(-1)
            circle2.append(marble)

        if marble % max(1, last_marble_2 // 40) == 0 or marble == last_marble_2:
            pct = marble * 100 // last_marble_2
            bar = "█" * (pct // 2) + "░" * (50 - pct // 2)
            yield {
                "type": "text",
                "lines": [
                    "Part 2 — 100× marbles",
                    "",
                    f"  Progress : {marble:,} / {last_marble_2:,}  ({pct}%)",
                    f"  [{bar}]",
                    "",
                    f"  High score so far: {max(scores2):,}",
                ],
                "delay": 80,
            }

    part2 = max(scores2)

    yield {
        "type": "text",
        "lines": [
            "Part 2 — Complete!",
            "",
            f"Marbles played : {last_marble_2:,}",
            f"Players        : {num_players}",
            f"Winning score  : {part2:,}",
            "",
            f"Answer: {part2}",
        ],
        "delay": 3000,
    }
