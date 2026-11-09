def largest_subsequence(digits, k):
    """
    Largest number made of k digits kept in their original order: pick the
    biggest digit that still leaves enough digits after it, then repeat.
    """
    result, start = [], 0
    for remaining in range(k, 0, -1):
        window = digits[start:len(digits) - remaining + 1]
        best = max(window)
        start += window.index(best) + 1
        result.append(best)
    return "".join(result)
