def state_after(state, step, n):
    """
    The state after n steps (n can be 1_000_000_000) when the process
    eventually repeats. State must be hashable: convert grids to a tuple
    of strings or a frozenset first.
    """
    seen = {}      # state -> index where it first appeared
    history = []   # history[i] is the state after i steps
    for i in range(n):
        if state in seen:
            cycle_start = seen[state]
            cycle_length = i - cycle_start
            return history[cycle_start + (n - cycle_start) % cycle_length]
        seen[state] = i
        history.append(state)
        state = step(state)
    return state
