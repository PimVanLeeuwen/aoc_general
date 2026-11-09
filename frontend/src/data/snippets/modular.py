from math import lcm


def crt(remainders, moduli):
    """
    Smallest t >= 0 with t % m == r for every (r, m), by sieving: once t fits
    the first few moduli, step by their lcm so it keeps fitting them.
    """
    t, step = 0, 1
    for remainder, modulus in zip(remainders, moduli):
        while t % modulus != remainder % modulus:
            t += step
        step = lcm(step, modulus)
    return t


# Other tools in this family:
#   lcm(*cycle_lengths)     when independent loops must line up (all ghosts at Z)
#   pow(a, -1, m)           modular inverse
#   pow(a, n, m)            fast modular power (n can be huge)
#   worry %= lcm(*divisors) keep numbers small while every divisibility test still works
