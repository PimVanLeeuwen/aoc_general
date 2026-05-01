"""
Day 05 - Doesn't He Have Intern-Elves For This?
Year: 2015

Classify strings as nice or naughty based on two different rule sets.
"""
import re


def is_nice_v1(s: str) -> bool:
    has_vowels    = sum(s.count(v) for v in "aeiou") >= 3
    has_double    = any(s[i] == s[i + 1] for i in range(len(s) - 1))
    no_forbidden  = not re.search(r"ab|cd|pq|xy", s)
    return has_vowels and has_double and no_forbidden


def is_nice_v2(s: str) -> bool:
    has_pair      = bool(re.search(r"(..).*\1", s))
    has_sandwich  = bool(re.search(r"(.).\1", s))
    return has_pair and has_sandwich


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")
    part1 = sum(is_nice_v1(s) for s in lines)
    part2 = sum(is_nice_v2(s) for s in lines)
    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Step through each string showing which rules it passes or fails."""
    lines = puzzle_input.strip().split("\n")
    nice_v1 = nice_v2 = 0

    for i, s in enumerate(lines):
        vowels   = sum(s.count(v) for v in "aeiou")
        double   = bool(re.search(r"(.)\1", s))
        forbid   = bool(re.search(r"ab|cd|pq|xy", s))
        pair     = bool(re.search(r"(..).*\1", s))
        sandwich = bool(re.search(r"(.).\1", s))

        v1 = vowels >= 3 and double and not forbid
        v2 = pair and sandwich
        nice_v1 += v1
        nice_v2 += v2

        def ok(b): return "pass" if b else "FAIL"

        yield {
            "type": "text",
            "lines": [
                f"String {i + 1}/{len(lines)}: {s}",
                "",
                "  Part 1 rules:",
                f"    Three vowels  : {ok(vowels >= 3)}  ({vowels} found)",
                f"    Double letter : {ok(double)}",
                f"    No forbidden  : {ok(not forbid)}",
                f"    => {'NICE' if v1 else 'naughty'}",
                "",
                "  Part 2 rules:",
                f"    Repeated pair : {ok(pair)}",
                f"    Sandwich      : {ok(sandwich)}",
                f"    => {'NICE' if v2 else 'naughty'}",
                "",
                f"  Running totals — Part 1: {nice_v1} nice  |  Part 2: {nice_v2} nice",
            ],
            "delay": 120,
        }