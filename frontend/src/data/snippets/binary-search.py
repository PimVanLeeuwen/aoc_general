def first_true(low, high, predicate):
    """
    Smallest x in [low, high] where predicate(x) is True, for a predicate that
    flips from False to True exactly once ('after how many bytes is the path
    blocked?', 'how much fuel can 1 trillion ore make?'). O(log n) calls.
    """
    while low < high:
        middle = (low + high) // 2
        if predicate(middle):
            high = middle
        else:
            low = middle + 1
    return low

# On a sorted list: bisect.bisect_left(values, x) is the same idea, built in.
