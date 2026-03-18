"""
Day 14 - Chocolate Charts
Year: 2018

Two Elves build an ever-growing recipe scoreboard by summing their current scores.
Part 1: the 10 scores immediately after N recipes.
Part 2: how many recipes appear before the digit-sequence of N first occurs.
"""


def solve(puzzle_input: str) -> tuple[str, str]:
    nr_puzzles = int(puzzle_input.strip())
    target = [int(d) for d in str(nr_puzzles)]
    n = len(target)

    scores = [3, 7]
    elves = [0, 1]
    part1 = part2 = None

    while part1 is None or part2 is None:
        s = scores[elves[0]] + scores[elves[1]]
        if s >= 10:
            scores.append(s // 10)
        scores.append(s % 10)
        for i in [0, 1]:
            elves[i] = (elves[i] + 1 + scores[elves[i]]) % len(scores)
        if part1 is None and len(scores) >= nr_puzzles + 10:
            part1 = "".join(str(d) for d in scores[nr_puzzles:nr_puzzles + 10])
        if part2 is None:
            for offset in [len(scores) - n, len(scores) - n - 1]:
                if offset >= 0 and scores[offset:offset + n] == target:
                    part2 = offset
                    break

    return part1, str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    nr_puzzles = int(puzzle_input.strip())
    target = [int(d) for d in str(nr_puzzles)]
    n = len(target)

    DIGIT_COLORS = {
        "0": "#1a3a1a", "1": "#1e4a1e", "2": "#226022", "3": "#267526",
        "4": "#2a8a2a", "5": "#2ea02e", "6": "#32b532", "7": "#36ca36",
        "8": "#3ae03a", "9": "#00ff41",
        "E": "#ffdd00",  # elf position
        "T": "#ff4444",  # target match highlight
    }

    WIDTH = 80  # cells shown per row

    def render(scores, elves, highlight_start=None):
        # Show the last WIDTH scores, highlighting elf positions and target
        start = max(0, len(scores) - WIDTH)
        row = []
        for i in range(start, start + WIDTH):
            if i >= len(scores):
                row.append(" ")
            elif i in elves:
                row.append("E")
            elif highlight_start is not None and highlight_start <= i < highlight_start + n:
                row.append("T")
            else:
                row.append(str(scores[i]))
        return row

    scores = [3, 7]
    elves = [0, 1]
    part1 = part2 = None

    yield {"type": "grid", "cells": [render(scores, set(elves))], "colors": DIGIT_COLORS, "delay": 200}

    step = 0
    while part1 is None or part2 is None:
        s = scores[elves[0]] + scores[elves[1]]
        if s >= 10:
            scores.append(s // 10)
        scores.append(s % 10)
        for i in [0, 1]:
            elves[i] = (elves[i] + 1 + scores[elves[i]]) % len(scores)
        if part1 is None and len(scores) >= nr_puzzles + 10:
            part1 = "".join(str(d) for d in scores[nr_puzzles:nr_puzzles + 10])
        if part2 is None:
            for offset in [len(scores) - n, len(scores) - n - 1]:
                if offset >= 0 and scores[offset:offset + n] == target:
                    part2 = offset
                    break
        step += 1
        if step <= 300:
            yield {"type": "grid", "cells": [render(scores, set(elves))], "colors": DIGIT_COLORS, "delay": 80}
        elif step % 5000 == 0:
            yield {"type": "grid", "cells": [render(scores, set(elves))], "colors": DIGIT_COLORS, "delay": 30}

    # Final frame: highlight the target sequence in-place
    yield {"type": "grid", "cells": [render(scores, set(), highlight_start=part2)], "colors": DIGIT_COLORS, "delay": 1000}
    yield {
        "type": "text",
        "lines": [
            "Chocolate Charts",
            "",
            f"Recipes generated : {len(scores):,}",
            f"Part 1 (10 after {nr_puzzles}): {part1}",
            f"Part 2 (target at) : {part2:,}",
        ],
        "delay": 4000,
    }
