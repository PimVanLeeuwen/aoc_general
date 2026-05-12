"""
Day 6 - Universal Orbit Map
Year: 2019

Count total orbits in a tree, then find shortest path between two nodes.
"""

from collections import defaultdict, deque


def build_tree(lines):
    """Parse orbit map into a parent dict and adjacency list."""
    parent = {}
    adj = defaultdict(list)
    for line in lines:
        a, b = line.split(")")
        parent[b] = a
        adj[a].append(b)
        adj[b].append(a)
    return parent, adj


def count_orbits(parent):
    """Count total direct + indirect orbits by walking each node to COM."""
    depth_cache = {}

    def depth(node):
        if node not in parent:
            return 0
        if node not in depth_cache:
            depth_cache[node] = 1 + depth(parent[node])
        return depth_cache[node]

    return sum(depth(node) for node in parent)


def transfers(adj, start, end):
    """BFS shortest path between two nodes in the orbit graph."""
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    lines = puzzle_input.strip().splitlines()
    parent, adj = build_tree(lines)

    part1 = count_orbits(parent)
    # Transfers between the objects YOU and SAN orbit, not YOU/SAN themselves
    part2 = transfers(adj, parent["YOU"], parent["SAN"])

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the orbit tree and path finding."""
    lines = puzzle_input.strip().splitlines()
    parent, adj = build_tree(lines)

    # Tree stats
    all_nodes = set(parent.keys()) | set(parent.values())
    leaves = [n for n in all_nodes if n not in set(parent.values())]

    yield {
        "type": "text",
        "lines": [
            "  Universal Orbit Map",
            "",
            f"  Objects: {len(all_nodes)}",
            f"  Orbits: {len(parent)}",
            f"  Leaves: {len(leaves)}",
        ],
        "delay": 600,
    }

    # Count orbits with depth visualization
    depth_cache = {}

    def depth(node):
        if node not in parent:
            return 0
        if node not in depth_cache:
            depth_cache[node] = 1 + depth(parent[node])
        return depth_cache[node]

    max_depth = 0
    total = 0
    for node in parent:
        d = depth(node)
        total += d
        max_depth = max(max_depth, d)

    # Show depth distribution
    dist = defaultdict(int)
    for node in parent:
        dist[depth(node)] += 1

    histogram_lines = []
    max_count = max(dist.values())
    bar_scale = 40 / max_count if max_count > 0 else 1
    step = max(1, max_depth // 15)
    for d in range(0, max_depth + 1, step):
        count = sum(dist.get(d + i, 0) for i in range(step))
        bar = "#" * int(count * bar_scale)
        histogram_lines.append(f"  {d:>3}-{d+step-1:<3} |{bar} {count}")

    yield {
        "type": "text",
        "lines": [
            "  Orbit depth distribution:",
            "",
        ] + histogram_lines + [
            "",
            f"  Max depth: {max_depth}",
            f"  Total orbits: {total}",
        ],
        "delay": 600,
    }

    # Part 2: show the path from YOU to SAN
    you_chain = []
    node = "YOU"
    while node in parent:
        node = parent[node]
        you_chain.append(node)

    san_chain = []
    node = "SAN"
    while node in parent:
        node = parent[node]
        san_chain.append(node)

    you_set = set(you_chain)
    common = None
    for node in san_chain:
        if node in you_set:
            common = node
            break

    you_to_common = you_chain[:you_chain.index(common)]
    san_to_common = san_chain[:san_chain.index(common)]
    path_len = len(you_to_common) + len(san_to_common)

    path_display = you_to_common[:5]
    if len(you_to_common) > 5:
        path_display.append("...")
    path_display.append(f"[{common}]")
    if len(san_to_common) > 5:
        path_display.append("...")
    path_display.extend(reversed(san_to_common[:5]))

    yield {
        "type": "text",
        "lines": [
            "  Path: YOU -> SAN",
            "",
            f"  YOU orbits: {parent['YOU']}",
            f"  SAN orbits: {parent['SAN']}",
            f"  Common ancestor: {common}",
            "",
            f"  Path: {' -> '.join(path_display)}",
            f"  Transfers: {path_len}",
        ],
        "delay": 600,
    }

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {total} total orbits",
            f"  Part 2: {path_len} orbital transfers",
        ],
        "delay": 500,
    }
