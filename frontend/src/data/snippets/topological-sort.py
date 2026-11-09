import heapq


def topological_order(nodes, edges):
    """
    Kahn's algorithm: an order where every (before, after) edge is respected.
    Ties are broken alphabetically (a common AoC rule). Raises on a cycle.
    """
    successors = {node: [] for node in nodes}
    incoming = {node: 0 for node in nodes}
    for before, after in edges:
        successors[before].append(after)
        incoming[after] += 1

    ready = [node for node in nodes if incoming[node] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for next_node in successors[node]:
            incoming[next_node] -= 1
            if incoming[next_node] == 0:
                heapq.heappush(ready, next_node)
    if len(order) != len(nodes):
        raise ValueError("the edges contain a cycle")
    return order
