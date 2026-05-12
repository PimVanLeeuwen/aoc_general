"""
Day 21 - Allergen Assessment
Year: 2020

Determine which ingredients can't contain allergens, then build the
canonical dangerous ingredient list sorted by allergen name.
"""


def parse_foods(text):
    """Parse each line into (ingredients_set, allergens_set)."""
    foods = []
    for line in text.strip().split("\n"):
        parts = line.split(" (contains ")
        ingredients = set(parts[0].split())
        allergens = set(parts[1].rstrip(")").replace(",", "").split())
        foods.append((ingredients, allergens))
    return foods


def identify_allergens(foods):
    """Map each allergen to its ingredient by intersecting candidate sets."""
    candidates = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in candidates:
                candidates[allergen] &= ingredients
            else:
                candidates[allergen] = set(ingredients)

    resolved = {}
    while candidates:
        found = False
        for allergen, possible in list(candidates.items()):
            if len(possible) == 1:
                ingredient = next(iter(possible))
                resolved[allergen] = ingredient
                del candidates[allergen]
                for other in candidates:
                    candidates[other].discard(ingredient)
                found = True
                break
        if not found:
            break

    return resolved


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    foods = parse_foods(puzzle_input)
    resolved = identify_allergens(foods)
    dangerous = set(resolved.values())

    # Part 1: count appearances of non-allergenic ingredients
    part1 = sum(
        1 for ingredients, _ in foods
        for ing in ingredients
        if ing not in dangerous
    )

    # Part 2: dangerous ingredients sorted by their allergen name
    part2 = ",".join(resolved[a] for a in sorted(resolved))

    return str(part1), part2


def visualize(puzzle_input: str):
    """Yield frames showing allergen identification process."""
    foods = parse_foods(puzzle_input)

    all_ingredients = set()
    all_allergens = set()
    for ingredients, allergens in foods:
        all_ingredients |= ingredients
        all_allergens |= allergens

    yield {
        "type": "text",
        "lines": [
            "  Allergen Assessment",
            "",
            f"  Foods: {len(foods)}",
            f"  Unique ingredients: {len(all_ingredients)}",
            f"  Allergens to identify: {len(all_allergens)}",
        ],
        "delay": 600,
    }

    # Show candidate narrowing
    candidates = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in candidates:
                candidates[allergen] &= ingredients
            else:
                candidates[allergen] = set(ingredients)

    lines = ["  Initial candidates per allergen:", ""]
    for allergen in sorted(candidates):
        names = ", ".join(sorted(candidates[allergen]))
        lines.append(f"  {allergen}: {names}")

    yield {
        "type": "text",
        "lines": lines,
        "delay": 800,
    }

    resolved = identify_allergens(foods)
    dangerous = set(resolved.values())

    part1 = sum(
        1 for ingredients, _ in foods
        for ing in ingredients
        if ing not in dangerous
    )
    part2 = ",".join(resolved[a] for a in sorted(resolved))

    result_lines = [
        "  ===================================",
        "  Results",
        "  ===================================",
        "",
        f"  Part 1: {part1} (safe ingredient appearances)",
        f"  Part 2: {part2}",
        "",
        "  Allergen mapping:",
    ]
    for allergen in sorted(resolved):
        result_lines.append(f"    {allergen} -> {resolved[allergen]}")

    yield {
        "type": "text",
        "lines": result_lines,
        "delay": 500,
    }
