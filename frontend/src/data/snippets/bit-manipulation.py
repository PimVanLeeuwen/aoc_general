def apply_mask(value, mask):
    """mask like 'XX1X0': 1 and 0 force that bit, X keeps the bit of value."""
    ones = int(mask.replace("X", "0"), 2)
    zeros = int(mask.replace("X", "1"), 2)
    return (value | ones) & zeros


# A set of up to ~60 small items as one int (cheap to hash, great as a search state):
#   add item i:  keys | (1 << i)      has item i:  keys >> i & 1
#   remove i:    keys & ~(1 << i)     size:        keys.bit_count()
# Binary strings: int("1011", 2) and f"{n:036b}" (zero-padded to 36 bits).
