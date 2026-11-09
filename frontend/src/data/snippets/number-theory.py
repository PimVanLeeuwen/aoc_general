from math import isqrt


def divisors(n):
    """All divisors of n in O(sqrt n)."""
    small = [d for d in range(1, isqrt(n) + 1) if n % d == 0]
    return sorted(set(small + [n // d for d in small]))


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def digits(n, base=10):
    """Digits of n, most significant first."""
    result = []
    while n:
        n, digit = divmod(n, base)
        result.append(digit)
    return result[::-1] or [0]


# int("1011", 2) parses any base; f"{n:b}", f"{n:o}", f"{n:x}" format one.
