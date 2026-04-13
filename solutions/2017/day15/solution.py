"""
Day 15 - Dueling Generators
Year: 2017

Part 1: Count matches in lowest 16 bits over 40 million pairs.
Part 2: Same, but with value filters and 5 million pairs.
"""

MOD = 2147483647
FA = 16807
FB = 48271

def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")
    A = int(lines[0].split()[-1])
    B = int(lines[1].split()[-1])

    a = A
    b = B
    matches = 0
    for _ in range(40_000_000):
        a = (a * FA) % MOD
        b = (b * FB) % MOD
        if (a & 0xFFFF) == (b & 0xFFFF):
            matches += 1

    part1 = matches

    def genA(val):
        while True:
            val = (val * FA) % MOD
            if val % 4 == 0:
                yield val

    def genB(val):
        while True:
            val = (val * FB) % MOD
            if val % 8 == 0:
                yield val

    gA = genA(A)
    gB = genB(B)

    matches = 0
    for _ in range(5_000_000):
        if (next(gA) & 0xFFFF) == (next(gB) & 0xFFFF):
            matches += 1

    part2 = matches

    return str(part1), str(part2)



def visualize(puzzle_input: str):
    """Visualize the first ~200 comparisons of the generators."""
    lines = puzzle_input.strip().split("\n")
    A = int(lines[0].split()[-1])
    B = int(lines[1].split()[-1])

    a = A
    b = B
    matches = 0

    for step in range(200):
        a = (a * FA) % MOD
        b = (b * FB) % MOD

        lowA = a & 0xFFFF
        lowB = b & 0xFFFF
        match = (lowA == lowB)
        if match:
            matches += 1

        # Convert to 16-bit binary strings
        bitsA = f"{lowA:016b}"
        bitsB = f"{lowB:016b}"

        # Build a small grid showing the bits
        grid = [
            list(bitsA),
            list(bitsB)
        ]

        yield {
            "type": "grid",
            "cells": grid,
            "colors": {
                "0": "#0f0f23",
                "1": "#00ff41"
            },
            "text": [
                f"Step {step+1}",
                f"A low16: {bitsA}",
                f"B low16: {bitsB}",
                "MATCH!" if match else "No match",
                f"Total matches so far: {matches}"
            ],
            "delay": 80
        }

    yield {
        "type": "text",
        "lines": [
            "Visualization complete",
            f"Matches in first 200 steps: {matches}",
            "Full solution uses 40M / 5M comparisons"
        ],
        "delay": 400
    }

