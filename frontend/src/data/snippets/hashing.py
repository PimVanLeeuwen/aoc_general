import hashlib


def md5_hex(text):
    return hashlib.md5(text.encode()).hexdigest()


def first_index_with_prefix(secret, prefix="00000"):
    """Lowest n where md5(secret + n) starts with prefix (brute force is the intended way)."""
    n = 0
    while not md5_hex(f"{secret}{n}").startswith(prefix):
        n += 1
    return n


def holiday_hash(text):
    """A custom rolling hash as puzzles define them: follow the steps literally."""
    value = 0
    for char in text:
        value = (value + ord(char)) * 17 % 256
    return value
