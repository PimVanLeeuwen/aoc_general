def count_paths(node, goal, graph, visited=frozenset()):
    """Count simple paths from node to goal, visiting each node at most once."""
    if node == goal:
        return 1
    visited = visited | {node}
    return sum(
        count_paths(next_node, goal, graph, visited)
        for next_node in graph[node]
        if next_node not in visited
    )


def longest_path(node, goal, graph, visited=None):
    """Longest simple path by backtracking. graph[node] = {next_node: distance}."""
    if node == goal:
        return 0
    visited = set() if visited is None else visited
    visited.add(node)
    best = float("-inf")
    for next_node, distance in graph[node].items():
        if next_node not in visited:
            best = max(best, distance + longest_path(next_node, goal, graph, visited))
    visited.remove(node)  # backtrack so other branches can use this node
    return best
