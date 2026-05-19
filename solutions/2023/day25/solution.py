"""
Day 25 - Snowverload
Year: 2023

Find a 3-edge cut in an undirected graph and return the
product of the two resulting component sizes.
"""

from collections import deque


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    # Build adjacency list
    adj = {}
    for line in puzzle_input.strip().split("\n"):
        src, targets = line.split(": ")
        targets = targets.split()
        if src not in adj:
            adj[src] = set()
        for t in targets:
            if t not in adj:
                adj[t] = set()
            adj[src].add(t)
            adj[t].add(src)

    nodes = list(adj)

    # Use Edmonds-Karp (BFS-based max flow) to find a min cut of size 3.
    # Pick node 0 as source, try each other node as sink.
    # When max flow = 3, the min cut separates the graph into two components.
    source = nodes[0]

    def bfs_path(capacity, source, sink):
        """Find an augmenting path using BFS. Return path or None."""
        visited = {source}
        queue = deque([(source, [source])])
        while queue:
            node, path = queue.popleft()
            for neighbor in capacity.get(node, {}):
                if neighbor not in visited and capacity[node][neighbor] > 0:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    if neighbor == sink:
                        return new_path
                    queue.append((neighbor, new_path))
        return None

    def max_flow_and_cut(source, sink):
        """Compute max flow and return (flow, reachable_from_source)."""
        # Build capacity graph
        capacity = {}
        for u in adj:
            capacity[u] = {}
        for u in adj:
            for v in adj[u]:
                capacity[u][v] = 1
                if v not in capacity:
                    capacity[v] = {}
                if u not in capacity[v]:
                    capacity[v][u] = 0

        flow = 0
        while True:
            path = bfs_path(capacity, source, sink)
            if not path:
                break
            flow += 1
            if flow > 3:
                return flow, None
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= 1
                capacity[v][u] += 1

        # BFS on residual to find source-side component
        visited = {source}
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for neighbor in capacity.get(node, {}):
                if neighbor not in visited and capacity[node][neighbor] > 0:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return flow, visited

    for sink in nodes[1:]:
        flow, reachable = max_flow_and_cut(source, sink)
        if flow == 3:
            part1 = len(reachable) * (len(nodes) - len(reachable))
            return str(part1), "⭐"

    return "0", "⭐"


def visualize(puzzle_input: str):
    """Yield frames showing graph analysis."""
    lines = puzzle_input.strip().split("\n")

    # Count unique nodes
    nodes = set()
    edges = 0
    for line in lines:
        src, targets = line.split(": ")
        targets = targets.split()
        nodes.add(src)
        nodes.update(targets)
        edges += len(targets)

    yield {
        "type": "text",
        "lines": [
            "  Snowverload",
            "",
            f"  Nodes: {len(nodes)}",
            f"  Edges: {edges}",
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
            f"  Part 1: {part1} (component product)",
            f"  Part 2: {part2}",
        ],
        "delay": 500,
    }
