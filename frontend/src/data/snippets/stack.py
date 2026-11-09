CLOSERS = {")": "(", "]": "[", "}": "{", ">": "<"}


def first_illegal(line):
    """First closing bracket that does not match, or None. Afterwards the stack holds what is still open."""
    stack = []
    for char in line:
        if char in CLOSERS.values():
            stack.append(char)
        elif not stack or stack.pop() != CLOSERS[char]:
            return char
    return None


def react(polymer):
    """Remove adjacent pairs like 'aA' until none are left, in one pass."""
    stack = []
    for unit in polymer:
        if stack and stack[-1] != unit and stack[-1].lower() == unit.lower():
            stack.pop()
        else:
            stack.append(unit)
    return "".join(stack)
