import json
import re


def ints(text):
    """All integers in a string, including negative ones."""
    return [int(number) for number in re.findall(r"-?\d+", text)]


def sections(text):
    """Blocks separated by a blank line (rules, then updates, ...)."""
    return text.strip().split("\n\n")


# One regex that matches several instruction kinds; check which one matched:
INSTRUCTION = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")


def sum_of_products(memory):
    total, enabled = 0, True
    for match in INSTRUCTION.finditer(memory):
        if match[0] == "do()":
            enabled = True
        elif match[0] == "don't()":
            enabled = False
        elif enabled:
            total += int(match[1]) * int(match[2])
    return total


def nested(line):
    """Nested lists like [1,[2,[3]]] are valid JSON."""
    return json.loads(line)

# 'key: value' lines: dict(line.split(": ", 1) for line in lines)
