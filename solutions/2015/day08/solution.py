"""
Day 08 - Matchsticks
Year: 2015

Count the difference between the number of characters in string literals
(code) and the number of characters they represent in memory.
Part 2: re-encode each string and measure the expansion.
"""
import ast
import re


def memory_len(s: str) -> int:
    """Number of characters the string literal represents in memory."""
    return len(ast.literal_eval(s))


def encoded_len(s: str) -> int:
    """Length of s after re-encoding: wrap in quotes, escape \\ and \"."""
    inner = s.replace("\\", "\\\\").replace('"', '\\"')
    return len(inner) + 2  # +2 for surrounding quotes


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    code_total   = sum(len(s) for s in lines)
    memory_total = sum(memory_len(s) for s in lines)
    encoded_total = sum(encoded_len(s) for s in lines)

    part1 = code_total - memory_total
    part2 = encoded_total - code_total

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Step through each string showing code, memory, and encoded lengths."""
    lines = puzzle_input.strip().split("\n")
    total = len(lines)
    running_p1 = running_p2 = 0

    for i, s in enumerate(lines):
        code_len = len(s)
        mem_len  = memory_len(s)
        enc_len  = encoded_len(s)
        diff_p1  = code_len - mem_len
        diff_p2  = enc_len - code_len
        running_p1 += diff_p1
        running_p2 += diff_p2

        # Annotate escape sequences in the string for display
        annotated = re.sub(r'\\\\|\\"|\\x[0-9a-f]{2}', lambda m: f"[{m.group()}]", s)

        yield {
            "type": "text",
            "lines": [
                f"String {i + 1}/{total}",
                "",
                f"  Code   : {s}",
                f"  Parsed : {annotated}",
                "",
                f"  Code length    : {code_len}",
                f"  Memory length  : {mem_len}   (code - memory = {diff_p1})",
                f"  Encoded length : {enc_len}   (encoded - code = {diff_p2})",
                "",
                f"  Running total — Part 1: {running_p1}  |  Part 2: {running_p2}",
            ],
            "delay": 150,
        }