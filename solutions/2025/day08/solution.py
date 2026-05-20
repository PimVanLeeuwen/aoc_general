"""
Day 8 - Box Clusters
Year: 2025

Group 3D boxes into clusters by proximity using a minimum
spanning tree approach. Part 1: product of 3 largest clusters
after 1000 edges. Part 2: last edge that connects everything.
"""

import math


def solve(puzzle_input: str) -> tuple[str, str]:
    boxes = [
        [int(x) for x in line.split(",")]
        for line in puzzle_input.split("\n") if line.strip()
    ]
    n = len(boxes)

    # Compute all pairwise Euclidean distances
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d = math.sqrt(sum((boxes[i][k] - boxes[j][k]) ** 2 for k in range(3)))
            edges.append((d, i, j))
    edges.sort()

    # Union-Find for Kruskal's algorithm
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    # Part 1: process first 1000 edges (by index), find 3 largest components
    for d, i, j in edges[:1000]:
        union(i, j)

    # Count component sizes
    from collections import Counter
    components = Counter(find(i) for i in range(n))
    sizes = sorted(components.values(), reverse=True)
    part1 = sizes[0] * sizes[1] * sizes[2]

    # Part 2: continue until one component, record the edge that does it
    part2 = 0
    for d, i, j in edges[1000:]:
        ci, cj = find(i), find(j)
        if ci != cj:
            union(i, j)
        num_components = len(set(find(x) for x in range(n)))
        if num_components == 1:
            part2 = boxes[i][0] * boxes[j][0]
            break

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    boxes = [
        [int(x) for x in line.split(",")]
        for line in puzzle_input.split("\n") if line.strip()
    ]

    yield {
        "type": "text",
        "lines": [
            "  Box Clusters",
            "",
            f"  Boxes: {len(boxes)}",
            f"  Dimensions: 3D coordinates",
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
            f"  Part 1: {part1} (top-3 cluster product)",
            f"  Part 2: {part2} (last bridge product)",
        ],
        "delay": 500,
    }
