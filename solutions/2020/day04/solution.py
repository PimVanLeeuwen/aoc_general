"""
Day 4 - Passport Processing
Year: 2020

Validate passport fields — first by presence, then by value constraints.
"""

import re

REQUIRED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def parse_passports(text):
    """Parse passport blocks separated by blank lines."""
    passports = []
    for block in text.strip().split("\n\n"):
        fields = {}
        for token in block.split():
            key, val = token.split(":")
            fields[key] = val
        passports.append(fields)
    return passports


def has_required_fields(passport):
    """Check all required fields are present."""
    return REQUIRED <= passport.keys()


def is_valid(passport):
    """Check all field values meet the constraints."""
    if not has_required_fields(passport):
        return False

    byr = int(passport["byr"])
    if len(passport["byr"]) != 4 or not (1920 <= byr <= 2002):
        return False

    iyr = int(passport["iyr"])
    if len(passport["iyr"]) != 4 or not (2010 <= iyr <= 2020):
        return False

    eyr = int(passport["eyr"])
    if len(passport["eyr"]) != 4 or not (2020 <= eyr <= 2030):
        return False

    hgt = passport["hgt"]
    if hgt.endswith("cm"):
        if not (150 <= int(hgt[:-2]) <= 193):
            return False
    elif hgt.endswith("in"):
        if not (59 <= int(hgt[:-2]) <= 76):
            return False
    else:
        return False

    if not re.fullmatch(r"#[0-9a-f]{6}", passport["hcl"]):
        return False

    if passport["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False

    if not re.fullmatch(r"\d{9}", passport["pid"]):
        return False

    return True


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    passports = parse_passports(puzzle_input)

    part1 = sum(1 for p in passports if has_required_fields(p))
    part2 = sum(1 for p in passports if is_valid(p))

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing passport validation."""
    passports = parse_passports(puzzle_input)

    yield {
        "type": "text",
        "lines": [
            "  Passport Processing",
            "",
            f"  Total passports: {len(passports)}",
            f"  Required fields: {', '.join(sorted(REQUIRED))}",
        ],
        "delay": 600,
    }

    part1 = sum(1 for p in passports if has_required_fields(p))
    part2 = sum(1 for p in passports if is_valid(p))

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Results",
            "  ===================================",
            "",
            f"  Part 1: {part1} (required fields present)",
            f"  Part 2: {part2} (all values valid)",
            f"  Rejected by fields: {len(passports) - part1}",
            f"  Rejected by values: {part1 - part2}",
        ],
        "delay": 500,
    }
