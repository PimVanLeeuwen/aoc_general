"""
Day 12 - JSAbacusFramework.io
Year: 2015

Sum all numbers in a JSON document, with optional filtering of "red" objects.
"""

import json
import re


def sum_numbers(obj, ignore_red=False):
    """Recursively sum all numbers in a JSON structure."""
    if isinstance(obj, int):
        return obj
    if isinstance(obj, str):
        return 0
    if isinstance(obj, list):
        return sum(sum_numbers(item, ignore_red) for item in obj)
    if isinstance(obj, dict):
        if ignore_red and "red" in obj.values():
            return 0
        return sum(sum_numbers(v, ignore_red) for v in obj.values())
    return 0


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    data = json.loads(puzzle_input.strip())

    part1 = str(sum_numbers(data))
    part2 = str(sum_numbers(data, ignore_red=True))

    return part1, part2


def visualize(puzzle_input: str):
    """Yield frames showing the recursive JSON traversal."""
    data = json.loads(puzzle_input.strip())

    # Collect stats during traversal
    stats = {"arrays": 0, "objects": 0, "numbers": 0, "strings": 0,
             "red_objects": 0, "running_p1": 0, "running_p2": 0, "depth": 0}
    frames = []

    def traverse(obj, depth, in_red_obj=False):
        stats["depth"] = max(stats["depth"], depth)

        if isinstance(obj, int):
            stats["numbers"] += 1
            stats["running_p1"] += obj
            if not in_red_obj:
                stats["running_p2"] += obj
            if stats["numbers"] % 200 == 0 or stats["numbers"] <= 20:
                frames.append(dict(stats))
            return
        if isinstance(obj, str):
            stats["strings"] += 1
            return
        if isinstance(obj, list):
            stats["arrays"] += 1
            for item in obj:
                traverse(item, depth + 1, in_red_obj)
            return
        if isinstance(obj, dict):
            stats["objects"] += 1
            is_red = "red" in obj.values()
            if is_red:
                stats["red_objects"] += 1
            for v in obj.values():
                traverse(v, depth + 1, in_red_obj or is_red)

    traverse(data, 0)
    frames.append(dict(stats))

    for i, s in enumerate(frames):
        is_last = i == len(frames) - 1
        bar_w = 40
        progress = min(s["numbers"] / max(frames[-1]["numbers"], 1), 1.0)
        bar = "█" * round(progress * bar_w) + "░" * (bar_w - round(progress * bar_w))

        lines = [
            "  Traversing JSON document",
            "",
            f"  Progress: [{bar}]",
            "",
            f"  Nodes visited:",
            f"    Objects:  {s['objects']:>6,}    (with \"red\": {s['red_objects']})",
            f"    Arrays:   {s['arrays']:>6,}",
            f"    Numbers:  {s['numbers']:>6,}",
            f"    Strings:  {s['strings']:>6,}",
            f"    Max depth: {s['depth']}",
            "",
            f"  Part 1 sum (all numbers):     {s['running_p1']:>10,}",
            f"  Part 2 sum (skip red objects): {s['running_p2']:>10,}",
        ]

        if is_last:
            lines.append("")
            lines.append(f"  ★ Part 1: {s['running_p1']}")
            lines.append(f"  ★ Part 2: {s['running_p2']}")

        yield {"type": "text", "lines": lines, "delay": 500 if is_last else 60}