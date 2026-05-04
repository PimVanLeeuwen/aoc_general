"""
Day 11 - Corporate Policy
Year: 2015

Find the next valid password by incrementing and checking corporate policy rules.
"""


def increment(pw: list[int]) -> None:
    i = len(pw) - 1
    while i >= 0:
        pw[i] += 1
        if pw[i] <= 25:
            return
        pw[i] = 0
        i -= 1


def skip_forbidden(pw: list[int]) -> None:
    """Jump past any forbidden letter (i=8, o=14, l=11) by incrementing it
    and zeroing everything to the right."""
    for i, c in enumerate(pw):
        if c in (8, 14, 11):
            pw[i] = c + 1
            for j in range(i + 1, len(pw)):
                pw[j] = 0
            return


def is_valid(pw: list[int]) -> bool:
    # No forbidden letters
    if any(c in (8, 14, 11) for c in pw):
        return False

    # Must have an increasing straight of 3
    has_straight = False
    for i in range(len(pw) - 2):
        if pw[i + 1] == pw[i] + 1 and pw[i + 2] == pw[i] + 2:
            has_straight = True
            break
    if not has_straight:
        return False

    # Must have at least two different non-overlapping pairs
    pairs = 0
    i = 0
    while i < len(pw) - 1:
        if pw[i] == pw[i + 1]:
            pairs += 1
            i += 2
        else:
            i += 1
    return pairs >= 2


def next_password(password: str) -> str:
    pw = [ord(c) - ord('a') for c in password]
    increment(pw)
    skip_forbidden(pw)
    while not is_valid(pw):
        increment(pw)
        skip_forbidden(pw)
    return "".join(chr(c + ord('a')) for c in pw)


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    password = puzzle_input.strip()

    part1 = next_password(password)
    part2 = next_password(part1)

    return part1, part2


def _check_rules(pw):
    """Return (straight_ok, no_forbidden, pairs_ok) booleans."""
    no_forbidden = not any(c in (8, 14, 11) for c in pw)

    has_straight = False
    for i in range(len(pw) - 2):
        if pw[i + 1] == pw[i] + 1 and pw[i + 2] == pw[i] + 2:
            has_straight = True
            break

    pairs = 0
    i = 0
    while i < len(pw) - 1:
        if pw[i] == pw[i + 1]:
            pairs += 1
            i += 2
        else:
            i += 1

    return has_straight, no_forbidden, pairs >= 2


def _pw_str(pw):
    return "".join(chr(c + ord('a')) for c in pw)


def visualize(puzzle_input: str):
    """Yield frames showing the password search process."""
    password = puzzle_input.strip()

    for part_num in (1, 2):
        pw = [ord(c) - ord('a') for c in password]
        increment(pw)
        skip_forbidden(pw)

        # Collect samples: first N attempts, then every Kth, then the answer
        samples = []
        attempts = 0
        while not is_valid(pw):
            attempts += 1
            if attempts <= 20 or attempts % 5000 == 0:
                samples.append((list(pw), attempts))
            increment(pw)
            skip_forbidden(pw)

        answer = _pw_str(pw)
        samples.append((list(pw), attempts + 1))

        pass_mark = "✓"
        fail_mark = "✗"

        for pw_snapshot, attempt in samples:
            straight, no_forb, pairs = _check_rules(pw_snapshot)
            current = _pw_str(pw_snapshot)
            is_answer = current == answer

            lines = [
                f"  Finding password #{part_num}",
                f"  Starting from: {password}",
                "",
                f"  Attempt {attempt:>7,}:  {current}",
                "",
                f"    {pass_mark if straight else fail_mark}  Increasing straight (abc, xyz, ...)",
                f"    {pass_mark if no_forb  else fail_mark}  No forbidden letters (i, o, l)",
                f"    {pass_mark if pairs    else fail_mark}  Two non-overlapping pairs",
            ]

            if is_answer:
                lines.append("")
                lines.append(f"  ★ Password #{part_num}: {answer}")

            delay = 300 if is_answer else 80
            yield {"type": "text", "lines": lines, "delay": delay}

        password = answer
