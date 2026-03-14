"""
Day 05 - Alchemical Reduction
Year: 2018

React a polymer by removing adjacent units of the same type but opposite polarity.
"""


def react(polymer: str) -> str:
    """Return reaction of a single polymer string."""
    stack = []
    for unit in polymer:
        if stack and stack[-1] != unit and stack[-1].lower() == unit.lower():
            stack.pop()
        else:
            stack.append(unit)
    return "".join(stack)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    polymer = puzzle_input.strip()

    reacted = react(polymer)
    part1 = len(reacted)

    unit_types = set(polymer.lower())
    part2 = min(
        len(react(polymer.replace(u, "").replace(u.upper(), "")))
        for u in unit_types
    )

    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    """Yield visualization frames for Day 05."""
    polymer = puzzle_input.strip()

    # --- Part 1: animate the reaction step by step (sample up to 80 chars) ---
    # Show on a truncated version so the animation is readable
    MAX_DISPLAY = 80
    sample = polymer[:MAX_DISPLAY] if len(polymer) > MAX_DISPLAY else polymer
    is_truncated = len(polymer) > MAX_DISPLAY

    yield {
        "type": "text",
        "lines": [
            "Part 1 — Reacting the polymer",
            f"(showing first {MAX_DISPLAY} units)" if is_truncated else "",
            "",
            sample,
            "",
            f"Full polymer length: {len(polymer):,}",
        ],
        "delay": 600,
    }

    # Animate the stack-based reaction on the sample
    stack = []
    reactions = 0
    frames_shown = 0
    MAX_FRAMES = 60

    for i, unit in enumerate(sample):
        if stack and stack[-1] != unit and stack[-1].lower() == unit.lower():
            stack.pop()
            reactions += 1
        else:
            stack.append(unit)

        if i % max(1, len(sample) // MAX_FRAMES) == 0 or i == len(sample) - 1:
            display = "".join(stack) if stack else "(empty)"
            yield {
                "type": "text",
                "lines": [
                    f"Part 1 — Processing unit {i+1}/{len(sample)}",
                    "",
                    f"Current unit : '{unit}'",
                    f"Reactions so far: {reactions}",
                    "",
                    "Stack:",
                    display[:80],
                    "",
                    f"Stack length: {len(stack)}",
                ],
                "delay": 80,
            }
            frames_shown += 1

    # Show full result
    full_reacted = react(polymer)
    yield {
        "type": "text",
        "lines": [
            "Part 1 — Reaction complete!",
            "",
            f"Original length : {len(polymer):,}",
            f"After reaction  : {len(full_reacted):,}",
            f"Units destroyed : {len(polymer) - len(full_reacted):,}",
            "",
            f"Answer: {len(full_reacted)}",
        ],
        "delay": 1200,
    }

    # --- Part 2: try removing each unit type ---
    unit_types = sorted(set(polymer.lower()))
    results = {}

    yield {
        "type": "text",
        "lines": [
            "Part 2 — Finding the problematic unit type",
            "",
            f"Unique unit types: {len(unit_types)}  ({', '.join(unit_types)})",
            "",
            "Testing each type...",
        ],
        "delay": 800,
    }

    best_unit = None
    best_len = len(polymer)

    for u in unit_types:
        stripped = polymer.replace(u, "").replace(u.upper(), "")
        result_len = len(react(stripped))
        results[u] = result_len
        if result_len < best_len:
            best_len = result_len
            best_unit = u

        # Build a bar chart of results so far
        bar_lines = [
            "Part 2 — Testing unit removal",
            "",
        ]
        for tested_u, tested_len in sorted(results.items()):
            bar = "█" * (tested_len * 30 // len(polymer))
            marker = " ← best so far" if tested_u == best_unit else ""
            bar_lines.append(f"  {tested_u}: {bar} {tested_len:,}{marker}")

        bar_lines += [
            "",
            f"Testing: '{u}' → {result_len:,} units",
        ]

        yield {
            "type": "text",
            "lines": bar_lines,
            "delay": 150,
        }

    yield {
        "type": "text",
        "lines": [
            "Part 2 — Done!",
            "",
            f"Removing '{best_unit}' / '{best_unit.upper()}' gives the shortest polymer.",
            "",
            f"Original length : {len(polymer):,}",
            f"Best result     : {best_len:,}",
            f"Units removed   : {len(polymer) - best_len:,}",
            "",
            f"Answer: {best_len}",
        ],
        "delay": 2000,
    }
