"""
Day 23 - LAN Party
Year: 2024

Find groups of interconnected computers. Part 1 counts
triangles with a 't' computer; part 2 finds the largest clique.
"""

from collections import defaultdict


def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    adj = defaultdict(set)
    for line in lines:
        a, b = line.split("-")
        adj[a].add(b)
        adj[b].add(a)

    computers = set(adj.keys())

    # Part 1: count triangles containing at least one 't' computer
    triangles = set()
    for c in computers:
        if not c.startswith("t"):
            continue
        neighbors = adj[c]
        for n1 in neighbors:
            for n2 in neighbors:
                if n1 < n2 and n2 in adj[n1]:
                    triangles.add(tuple(sorted([c, n1, n2])))

    part1 = len(triangles)

    # Part 2: find the largest clique (greedy approach)
    best_clique = set()
    for comp in computers:
        clique = {comp}
        for other in sorted(computers):
            if all(other in adj[member] for member in clique):
                clique.add(other)
        if len(clique) > len(best_clique):
            best_clique = clique

    part2 = ",".join(sorted(best_clique))

    return str(part1), part2


def visualize(puzzle_input: str):
    lines = puzzle_input.strip().split("\n")

    adj = defaultdict(set)
    for line in lines:
        a, b = line.split("-")
        adj[a].add(b)
        adj[b].add(a)

    yield {
        "type": "text",
        "lines": [
            "  LAN Party",
            "",
            f"  Connections: {len(lines)}",
            f"  Computers: {len(adj)}",
        ],
        "delay": 600,
    }

    part1, part2 = solve(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (triangles with 't')",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
