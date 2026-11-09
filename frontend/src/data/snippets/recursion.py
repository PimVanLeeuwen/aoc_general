import sys

sys.setrecursionlimit(10_000)  # deep inputs can exceed Python's default of 1000


def evaluate(name, jobs):
    """Evaluate an expression tree: jobs = {'root': ('a', '+', 'b'), 'a': 5, 'b': 3}."""
    job = jobs[name]
    if isinstance(job, int):
        return job
    left, operator, right = job
    a, b = evaluate(left, jobs), evaluate(right, jobs)
    return {"+": a + b, "-": a - b, "*": a * b, "/": a // b}[operator]


def compare(left, right):
    """Order nested lists of ints (parse lines with json.loads). Negative if left < right."""
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    for a, b in zip(left, right):
        if (result := compare(a, b)) != 0:
            return result
    return len(left) - len(right)

# Sort with it: sorted(packets, key=functools.cmp_to_key(compare))
