"""
Day 22 - Wizard Simulator 20XX
Year: 2015

Find the minimum mana to defeat the boss using spells with timed effects.
Uses BFS/priority queue (Dijkstra) on game states.
"""

import heapq

SPELLS = [
    ("Magic Missile", 53),
    ("Drain", 73),
    ("Shield", 113),
    ("Poison", 173),
    ("Recharge", 229),
]


def parse_boss(text):
    nums = []
    for line in text.strip().splitlines():
        nums.append(int(line.split(": ")[1]))
    return nums[0], nums[1]  # hp, damage


def find_min_mana(boss_hp, boss_dmg, hard_mode=False):
    """Dijkstra over game states to find minimum mana spent to win."""
    # State: (mana_spent, player_hp, player_mana, boss_hp, shield_t, poison_t, recharge_t)
    initial = (0, 50, 500, boss_hp, 0, 0, 0)
    heap = [initial]
    seen = set()

    while heap:
        mana_spent, hp, mana, b_hp, shield_t, poison_t, recharge_t = heapq.heappop(heap)

        # Prune visited states
        state_key = (hp, mana, b_hp, shield_t, poison_t, recharge_t)
        if state_key in seen:
            continue
        seen.add(state_key)

        # === PLAYER TURN ===

        # Hard mode: lose 1 HP at start of player turn
        if hard_mode:
            hp -= 1
            if hp <= 0:
                continue

        # Apply effects at start of player turn
        armor = 0
        if shield_t > 0:
            armor = 7
            shield_t -= 1
        if poison_t > 0:
            b_hp -= 3
            poison_t -= 1
        if recharge_t > 0:
            mana += 101
            recharge_t -= 1

        # Check if boss died from effects
        if b_hp <= 0:
            return mana_spent

        # Try each spell
        for spell_name, spell_cost in SPELLS:
            if mana < spell_cost:
                continue

            new_hp = hp
            new_mana = mana - spell_cost
            new_b_hp = b_hp
            new_shield = shield_t
            new_poison = poison_t
            new_recharge = recharge_t
            new_spent = mana_spent + spell_cost

            if spell_name == "Magic Missile":
                new_b_hp -= 4
            elif spell_name == "Drain":
                new_b_hp -= 2
                new_hp += 2
            elif spell_name == "Shield":
                if shield_t > 0:
                    continue
                new_shield = 6
            elif spell_name == "Poison":
                if poison_t > 0:
                    continue
                new_poison = 6
            elif spell_name == "Recharge":
                if recharge_t > 0:
                    continue
                new_recharge = 5

            # Check if boss died from spell
            if new_b_hp <= 0:
                return new_spent

            # === BOSS TURN ===

            # Apply effects at start of boss turn
            boss_armor = 0
            if new_shield > 0:
                boss_armor = 7
                new_shield -= 1
            if new_poison > 0:
                new_b_hp -= 3
                new_poison -= 1
            if new_recharge > 0:
                new_mana += 101
                new_recharge -= 1

            # Check if boss died from effects
            if new_b_hp <= 0:
                return new_spent

            # Boss attacks
            damage = max(1, boss_dmg - boss_armor)
            new_hp -= damage

            if new_hp <= 0:
                continue  # Player died

            heapq.heappush(heap, (
                new_spent, new_hp, new_mana, new_b_hp,
                new_shield, new_poison, new_recharge
            ))

    return -1  # No solution found


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    boss_hp, boss_dmg = parse_boss(puzzle_input)

    part1 = find_min_mana(boss_hp, boss_dmg, hard_mode=False)
    part2 = find_min_mana(boss_hp, boss_dmg, hard_mode=True)

    return str(part1), str(part2)


def visualize(puzzle_input: str):
    """Yield frames showing the optimal spell sequence."""
    boss_hp, boss_dmg = parse_boss(puzzle_input)

    # Find the optimal spell sequence by tracking paths
    initial = (0, 50, 500, boss_hp, 0, 0, 0, [])
    heap = [initial]
    seen = set()
    best_sequence = None

    while heap:
        mana_spent, hp, mana, b_hp, shield_t, poison_t, recharge_t, spells = heapq.heappop(heap)

        state_key = (hp, mana, b_hp, shield_t, poison_t, recharge_t)
        if state_key in seen:
            continue
        seen.add(state_key)

        armor = 0
        if shield_t > 0:
            armor = 7
            shield_t -= 1
        if poison_t > 0:
            b_hp -= 3
            poison_t -= 1
        if recharge_t > 0:
            mana += 101
            recharge_t -= 1

        if b_hp <= 0:
            best_sequence = spells
            break

        for spell_name, spell_cost in SPELLS:
            if mana < spell_cost:
                continue

            new_hp = hp
            new_mana = mana - spell_cost
            new_b_hp = b_hp
            new_shield = shield_t
            new_poison = poison_t
            new_recharge = recharge_t
            new_spent = mana_spent + spell_cost

            if spell_name == "Magic Missile":
                new_b_hp -= 4
            elif spell_name == "Drain":
                new_b_hp -= 2
                new_hp += 2
            elif spell_name == "Shield":
                if shield_t > 0:
                    continue
                new_shield = 6
            elif spell_name == "Poison":
                if poison_t > 0:
                    continue
                new_poison = 6
            elif spell_name == "Recharge":
                if recharge_t > 0:
                    continue
                new_recharge = 5

            if new_b_hp <= 0:
                best_sequence = spells + [spell_name]
                break

            boss_armor = 0
            if new_shield > 0:
                boss_armor = 7
                new_shield -= 1
            if new_poison > 0:
                new_b_hp -= 3
                new_poison -= 1
            if new_recharge > 0:
                new_mana += 101
                new_recharge -= 1

            if new_b_hp <= 0:
                best_sequence = spells + [spell_name]
                break

            damage = max(1, boss_dmg - boss_armor)
            new_hp -= damage

            if new_hp <= 0:
                continue

            heapq.heappush(heap, (
                new_spent, new_hp, new_mana, new_b_hp,
                new_shield, new_poison, new_recharge,
                spells + [spell_name]
            ))

        if best_sequence is not None:
            break

    if not best_sequence:
        yield {"type": "text", "lines": ["  No winning strategy found!"], "delay": 500}
        return

    # Replay the optimal fight
    yield {
        "type": "text",
        "lines": [
            "  Wizard Simulator 20XX",
            "",
            f"  Boss: {boss_hp} HP, {boss_dmg} DMG",
            f"  Player: 50 HP, 500 Mana",
            "",
            f"  Searching for optimal spell sequence...",
            f"  States explored: {len(seen):,}",
        ],
        "delay": 800,
    }

    # Simulate the winning fight step by step
    p_hp, p_mana = 50, 500
    b_hp_cur = boss_hp
    shield_t, poison_t, recharge_t = 0, 0, 0
    total_spent = 0

    for turn, spell_name in enumerate(best_sequence):
        spell_cost = dict(SPELLS)[spell_name]

        # Apply effects (player turn)
        effects_lines = []
        armor = 0
        if shield_t > 0:
            armor = 7
            shield_t -= 1
            effects_lines.append(f"    Shield active (armor +7, {shield_t} left)")
        if poison_t > 0:
            b_hp_cur -= 3
            poison_t -= 1
            effects_lines.append(f"    Poison deals 3 dmg ({poison_t} left)")
        if recharge_t > 0:
            p_mana += 101
            recharge_t -= 1
            effects_lines.append(f"    Recharge +101 mana ({recharge_t} left)")

        # Cast spell
        p_mana -= spell_cost
        total_spent += spell_cost

        if spell_name == "Magic Missile":
            b_hp_cur -= 4
        elif spell_name == "Drain":
            b_hp_cur -= 2
            p_hp += 2
        elif spell_name == "Shield":
            shield_t = 6
        elif spell_name == "Poison":
            poison_t = 6
        elif spell_name == "Recharge":
            recharge_t = 5

        lines = [
            f"  === Round {turn + 1} ===",
            "",
            f"  Player: {p_hp} HP, {armor} ARM, {p_mana} mana",
            f"  Boss:   {b_hp_cur} HP",
            "",
        ]
        if effects_lines:
            lines.append("  Effects:")
            lines.extend(effects_lines)
            lines.append("")
        lines.append(f"  -> Cast {spell_name} ({spell_cost} mana)")
        lines.append(f"  Total mana spent: {total_spent}")

        if b_hp_cur <= 0:
            lines.append("")
            lines.append("  Boss defeated!")
            yield {"type": "text", "lines": lines, "delay": 600}
            break

        # Boss turn effects
        if shield_t > 0:
            armor = 7
            shield_t -= 1
        else:
            armor = 0
        if poison_t > 0:
            b_hp_cur -= 3
            poison_t -= 1
        if recharge_t > 0:
            p_mana += 101
            recharge_t -= 1

        if b_hp_cur <= 0:
            lines.append("")
            lines.append("  Poison kills the boss!")
            yield {"type": "text", "lines": lines, "delay": 600}
            break

        damage = max(1, boss_dmg - armor)
        p_hp -= damage
        lines.append(f"  Boss attacks for {damage} damage")

        yield {"type": "text", "lines": lines, "delay": 400}

    yield {
        "type": "text",
        "lines": [
            "  ===================================",
            "  Victory!",
            "  ===================================",
            "",
            f"  Optimal sequence: {' -> '.join(best_sequence)}",
            f"  Total mana spent: {total_spent}",
            "",
            f"  Part 1: {total_spent}",
        ],
        "delay": 500,
    }