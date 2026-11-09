from collections import deque


def search_states(start, is_goal, moves, canonical=lambda state: state):
    """
    BFS where every node is a complete puzzle state. States must be hashable
    (tuples or frozensets). canonical() maps equivalent states to one key,
    for example sorting interchangeable pairs, which prunes the search a lot.
    """
    queue = deque([(start, 0)])
    seen = {canonical(start)}
    while queue:
        state, steps = queue.popleft()
        if is_goal(state):
            return steps
        for next_state in moves(state):
            key = canonical(next_state)
            if key not in seen:
                seen.add(key)
                queue.append((next_state, steps + 1))
    return None
