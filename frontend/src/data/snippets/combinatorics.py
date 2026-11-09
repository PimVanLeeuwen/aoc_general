from itertools import combinations, permutations, product

# Every ordering (n! grows fast, fine up to about 10 items):
#   for order in permutations(cities): ...
# Every unordered pair once:
#   for a, b in combinations(points, 2): ...
# Every choice per slot (operators, bits):
#   for operators in product("+*", repeat=len(numbers) - 1): ...


def best_order(items, score):
    """The ordering with the highest score, by trying them all."""
    return max(permutations(items), key=score)


def smallest_groups_with_sum(items, target):
    """All smallest-size groups that add up to target (try small sizes first)."""
    for size in range(1, len(items) + 1):
        groups = [group for group in combinations(items, size) if sum(group) == target]
        if groups:
            return groups
    return []
