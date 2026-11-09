def run(program, registers):
    """
    Small assembly interpreter. program is a list of lines like 'cpy 41 a';
    an argument is a register name or a number. Jumps are relative.
    """
    pc = 0

    def value(argument):
        return registers[argument] if argument in registers else int(argument)

    while 0 <= pc < len(program):
        operation, *args = program[pc].split()
        match operation:
            case "cpy":
                registers[args[1]] = value(args[0])
            case "inc":
                registers[args[0]] += 1
            case "dec":
                registers[args[0]] -= 1
            case "jnz":
                if value(args[0]) != 0:
                    pc += value(args[1])
                    continue
        pc += 1
    return registers

# Infinite-loop detection: keep a set of visited pc values (or (pc, registers) states).
