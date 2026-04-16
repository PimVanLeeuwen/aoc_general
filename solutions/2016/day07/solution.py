"""
Day 07 - Internet Protocol Version 7
Year: 2016

Determine which IPv7 addresses support TLS and SSL by detecting ABBA and ABA/BAB patterns.
"""

def has_abba(s: str) -> bool:
    """Return True if the string contains an ABBA pattern."""
    return any(a != b and a == d and b == c for a, b, c, d in zip(s, s[1:], s[2:], s[3:]))

def find_aba(s: str):
    """Return all ABA patterns in the string."""
    return [s[i:i+3] for i in range(len(s)-2) if s[i] == s[i+2] and s[i] != s[i+1]]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    tls_count = 0
    ssl_count = 0

    for line in lines:
        # Split into supernet and hypernet sequences
        parts = []
        buf = ""
        inside = False
        supernets = []
        hypernets = []

        for ch in line:
            if ch == "[":
                if buf:
                    supernets.append(buf) if not inside else hypernets.append(buf)
                buf = ""
                inside = True
            elif ch == "]":
                if buf:
                    hypernets.append(buf)
                buf = ""
                inside = False
            else:
                buf += ch
        if buf:
            supernets.append(buf) if not inside else hypernets.append(buf)

        # Part 1: TLS
        if any(has_abba(s) for s in supernets) and not any(has_abba(h) for h in hypernets):
            tls_count += 1

        # Part 2: SSL
        abas = [aba for s in supernets for aba in find_aba(s)]
        babs = {aba[1] + aba[0] + aba[1] for aba in abas}

        if any(bab in h for h in hypernets for bab in babs):
            ssl_count += 1

    return str(tls_count), str(ssl_count)


# ── Optional visualizer ────────────────────────────────────────────────────────
# Uncomment and implement to enable the Visualization tab in the portfolio.
#
# def visualize(puzzle_input: str):
#     """Yield visualization frames (up to ~500 recommended)."""
#     lines = puzzle_input.strip().split("\n")
#
#     # Grid frame – renders as a pixel canvas:
#     yield {
#         "type": "grid",
#         "cells": [list(row) for row in lines],
#         "colors": {"#": "#00ff41", ".": "#0f0f23"},   # cell → hex color
#         "delay": 100,   # ms before advancing to next frame
#     }
#
#     # Text frame – renders as monospace text:
#     yield {
#         "type": "text",
#         "lines": ["Step 1", "Value: 42"],
#         "delay": 300,
#     }
