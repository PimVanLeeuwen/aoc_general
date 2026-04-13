"""
Day 12 - Digital Plumber
Year: 2017

Part 1: Size of the group containing program ID 0.
Part 2: Total number of groups (connected components).
"""

def solve(puzzle_input: str) -> tuple[str, str]:
    lines = puzzle_input.strip().split("\n")

    graph = {}

    # Parse input
    for line in lines:
        left, right = line.split("<->")
        node = int(left.strip())
        neighbors = [int(x) for x in right.split(",")]
        graph[node] = neighbors

    # BFS/DFS helper
    def explore(start, visited):
        stack = [start]
        while stack:
            n = stack.pop()
            if n not in visited:
                visited.add(n)
                stack.extend(graph[n])
        return visited

    # Part 1: size of group containing 0
    visited = explore(0, set())
    part1 = len(visited)

    # Part 2: count connected components
    all_visited = set()
    part2 = 0

    for node in graph:
        if node not in all_visited:
            explore(node, all_visited)
            part2 += 1

    return str(part1), str(part2)
