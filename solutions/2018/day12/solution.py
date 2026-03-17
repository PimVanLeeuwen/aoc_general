"""
Day 12 - Subterranean Sustainability
Year: 2018

Simulate cellular-automaton plant growth in a row of pots.
Part 1: sum of plant-pot indices after 20 generations.
Part 2: sum after 50 billion generations (detected via pattern-shift cycle).
"""


def parse(puzzle_input: str):
    lines = puzzle_input.strip().splitlines()
    initial = lines[0].split(": ")[1]
    state = {i for i, c in enumerate(initial) if c == "#"}
    rules = {}
    for line in lines[2:]:
        pattern, result = line.split(" => ")
        rules[pattern] = result
    return state, rules


def step(state: set, rules: dict) -> set:
    lo, hi = min(state) - 2, max(state) + 2
    return {
        i for i in range(lo, hi + 1)
        if rules.get("".join("#" if i + d in state else "." for d in range(-2, 3)), ".") == "#"
    }


def solve(puzzle_input: str) -> tuple[str, str]:
    state, rules = parse(puzzle_input)

    # Part 1: 20 generations
    s = state.copy()
    for _ in range(20):
        s = step(s, rules)
    part1 = sum(s)

    # Part 2: 50 billion generations — detect when the pattern just shifts each gen
    s = state.copy()
    for gen in range(1, 50000000000 + 1):
        ns = step(s, rules)
        offset_old = min(s)
        offset_new = min(ns)
        if frozenset(p - offset_new for p in ns) == frozenset(p - offset_old for p in s):
            shift_per_gen = offset_new - offset_old
            remaining = 50_000_000_000 - gen
            part2 = sum(p + shift_per_gen * remaining for p in ns)
            break
        s = ns
    else:
        part2 = sum(s)

    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    state, rules = parse(puzzle_input)

    COLORS = {"#": "#00ff41", ".": "#0a1a0a"}
    WIDTH = 80

    def render(s: set, center: int) -> list[str]:
        return ["#" if i in s else "." for i in range(center - WIDTH // 2, center + WIDTH // 2)]

    center = (min(state) + max(state)) // 2

    yield {"type": "grid", "cells": [render(state, center)], "colors": COLORS, "delay": 300}
    yield {
        "type": "text",
        "lines": ["Generation 0 (initial state)", f"Plants: {len(state)}  Sum: {sum(state)}"],
        "delay": 500,
    }

    # Show first 20 generations
    s = state.copy()
    for gen in range(1, 21):
        s = step(s, rules)
        if s:
            center = (min(s) + max(s)) // 2
        yield {"type": "grid", "cells": [render(s, center)], "colors": COLORS, "delay": 200}

    yield {
        "type": "text",
        "lines": [
            "After 20 generations",
            "",
            f"Plants alive : {len(s)}",
            f"Index range  : {min(s)} … {max(s)}",
            f"Part 1 answer: {sum(s)}",
        ],
        "delay": 2000,
    }

    # Detect the shift cycle for Part 2
    s = state.copy()
    for gen in range(1, 50_000_000_000 + 1):
        ns = step(s, rules)
        offset_old = min(s)
        offset_new = min(ns)
        if frozenset(p - offset_new for p in ns) == frozenset(p - offset_old for p in s):
            shift = offset_new - offset_old
            remaining = 50_000_000_000 - gen
            part2 = sum(p + shift * remaining for p in ns)
            yield {
                "type": "text",
                "lines": [
                    f"Cycle detected at generation {gen}",
                    "",
                    f"Pattern shifts +{shift} per generation",
                    f"Remaining gens : {remaining:,}",
                    f"Part 2 answer  : {part2}",
                ],
                "delay": 4000,
            }
            break
        s = ns
