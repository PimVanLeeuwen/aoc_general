def resolve(candidates):
    """
    candidates = {name: set of possible values}. Repeatedly fix a name that
    has one option left and remove that value from all others.
    """
    candidates = {name: set(values) for name, values in candidates.items()}
    solved = {}
    while candidates:
        name = next((n for n, values in candidates.items() if len(values) == 1), None)
        if name is None:
            raise ValueError(f"stuck, still ambiguous: {candidates}")
        value = candidates.pop(name).pop()
        solved[name] = value
        for values in candidates.values():
            values.discard(value)
    return solved
