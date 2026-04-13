"""
Day 25 - Four-Dimensional Adventure
Year: 2018

You are given a list of 4‑dimensional points. Two points belong to the same
constellation if their Manhattan distance is at most 3, or if they can be
connected through a chain of such close points. The task is to count how many
constellations (connected components) exist.
"""

def dist(a, b):
    """Return Manhattan distance in 4d"""
    return sum(abs(a[i] - b[i]) for i in range(4))

def dfs(points, visited, start):
    """dfs over a 4d Manhattan grid"""
    stack = [start]
    visited[start] = True
    n = len(points)
    while stack:
        i = stack.pop()
        for j in range(n):
            if not visited[j] and dist(points[i], points[j]) <= 3:
                visited[j] = True
                stack.append(j)

def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().split("\n")

    # Parse points
    points = [tuple(map(int, line.split(","))) for line in lines]

    visited = [False] * len(points)

    # Count connected components
    part1 = 0
    for i in range(len(points)):
        if not visited[i]:
            dfs(points, visited, i)
            part1 += 1

    # Part 1
    part1 = str(part1)

    # Part 2
    part2 = ""

    return part1, part2


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
