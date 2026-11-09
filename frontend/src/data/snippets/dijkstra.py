import heapq


def dijkstra(start, is_goal, neighbors):
    """
    Lowest total cost from start to a goal. neighbors(node) yields
    (next_node, step_cost) with step_cost >= 0. A node can be a whole
    state, e.g. (row, col, direction, steps_in_a_row).
    """
    best = {start: 0}
    heap = [(0, start)]
    while heap:
        cost, node = heapq.heappop(heap)
        if is_goal(node):
            return cost
        if cost > best[node]:
            continue  # stale entry: a cheaper path to node was found already
        for next_node, step_cost in neighbors(node):
            new_cost = cost + step_cost
            if new_cost < best.get(next_node, float("inf")):
                best[next_node] = new_cost
                heapq.heappush(heap, (new_cost, next_node))
    return None
