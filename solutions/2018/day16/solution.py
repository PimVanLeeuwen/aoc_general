"""
Day 16 - Chronal Classification
Year: 2018

Reverse-engineer CPU opcodes by analyzing sample executions, then run a test program.
Part 1: Count samples that behave like 3+ opcodes.
Part 2: Determine opcode mappings and execute test program.
"""

# Define all 16 operations
def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]

def addi(regs, a, b, c):
    regs[c] = regs[a] + b

def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]

def muli(regs, a, b, c):
    regs[c] = regs[a] * b

def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]

def bani(regs, a, b, c):
    regs[c] = regs[a] & b

def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]

def bori(regs, a, b, c):
    regs[c] = regs[a] | b

def setr(regs, a, b, c):
    regs[c] = regs[a]

def seti(regs, a, b, c):
    regs[c] = a

def gtir(regs, a, b, c):
    regs[c] = 1 if a > regs[b] else 0

def gtri(regs, a, b, c):
    regs[c] = 1 if regs[a] > b else 0

def gtrr(regs, a, b, c):
    regs[c] = 1 if regs[a] > regs[b] else 0

def eqir(regs, a, b, c):
    regs[c] = 1 if a == regs[b] else 0

def eqri(regs, a, b, c):
    regs[c] = 1 if regs[a] == b else 0

def eqrr(regs, a, b, c):
    regs[c] = 1 if regs[a] == regs[b] else 0


ALL_OPS = [addr, addi, mulr, muli, banr, bani, borr, bori,
           setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def parse_input(puzzle_input: str):
    """Parse input into samples and test program."""
    lines = puzzle_input.strip().split('\n')
    
    samples = []
    i = 0
    
    # Parse samples (format: Before, instruction, After, blank line)
    while i < len(lines):
        if not lines[i].startswith('Before:'):
            break
        
        # Parse Before
        before = eval(lines[i].split(': ')[1])
        
        # Parse instruction
        instruction = list(map(int, lines[i + 1].split()))
        
        # Parse After
        after = eval(lines[i + 2].split(': ')[1])
        
        samples.append((before, instruction, after))
        i += 3  # Move past Before, instruction, After
        
        # Skip blank line(s) after sample
        while i < len(lines) and not lines[i].strip():
            i += 1
    
    # Skip blank lines between sections
    while i < len(lines) and not lines[i].strip():
        i += 1
    
    # Parse test program
    program = []
    while i < len(lines):
        if lines[i].strip():
            program.append(list(map(int, lines[i].split())))
        i += 1
    
    return samples, program


def test_opcode(op_func, before, instruction, after):
    """Test if an opcode function produces the expected result."""
    _, a, b, c = instruction
    regs = list(before)
    op_func(regs, a, b, c)
    return regs == list(after)


def count_matching_opcodes(sample):
    """Count how many opcodes could produce the sample's result."""
    before, instruction, after = sample
    count = 0
    for op in ALL_OPS:
        if test_opcode(op, before, instruction, after):
            count += 1
    return count


def determine_opcode_mapping(samples):
    """Deduce which opcode number corresponds to which operation."""
    # For each opcode number, track which operations are possible
    possible = {i: set(ALL_OPS) for i in range(16)}
    
    # Eliminate impossible mappings based on samples
    for before, instruction, after in samples:
        opcode_num = instruction[0]
        for op in ALL_OPS:
            if not test_opcode(op, before, instruction, after):
                possible[opcode_num].discard(op)
    
    # Deduce final mapping using constraint propagation
    mapping = {}
    while len(mapping) < 16:
        # Find opcodes with only one possibility
        for opcode_num, ops in possible.items():
            if len(ops) == 1 and opcode_num not in mapping:
                op = next(iter(ops))
                mapping[opcode_num] = op
                # Remove this operation from all other opcodes
                for other_num in possible:
                    if other_num != opcode_num:
                        possible[other_num].discard(op)
    
    return mapping


def execute_program(program, mapping):
    """Execute test program with determined opcode mapping."""
    regs = [0, 0, 0, 0]
    for instruction in program:
        opcode_num, a, b, c = instruction
        mapping[opcode_num](regs, a, b, c)
    return regs[0]


def solve(puzzle_input: str) -> tuple[str, str]:
    """Return (part1_answer, part2_answer)."""
    samples, program = parse_input(puzzle_input)
    
    # Part 1: Count samples behaving like 3+ opcodes
    part1 = sum(1 for sample in samples if count_matching_opcodes(sample) >= 3)
    
    # Part 2: Determine mapping and execute program
    mapping = determine_opcode_mapping(samples)
    part2 = execute_program(program, mapping)
    
    return str(part1), str(part2)


# ── Optional visualizer ────────────────────────────────────────────────────────

def visualize(puzzle_input: str):
    """Yield visualization frames for Day 16."""
    samples, program = parse_input(puzzle_input)
    
    # Show initial analysis
    yield {
        "type": "text",
        "lines": [
            "Chronal Classification",
            "",
            f"Analyzing {len(samples)} samples...",
            f"Test program: {len(program)} instructions",
        ],
        "delay": 500,
    }
    
    # Part 1: Analyze samples
    three_plus = 0
    total_shown = 0
    max_show = 10
    
    for i, sample in enumerate(samples):
        count = count_matching_opcodes(sample)
        if count >= 3:
            three_plus += 1
        
        if total_shown < max_show and (count >= 3 or i < 5):
            before, instruction, after = sample
            yield {
                "type": "text",
                "lines": [
                    f"Sample {i + 1}:",
                    f"  Before: {before}",
                    f"  Instruction: {instruction}",
                    f"  After: {after}",
                    f"  Matches {count} opcodes",
                ],
                "delay": 200,
            }
            total_shown += 1
    
    yield {
        "type": "text",
        "lines": [
            "Part 1 Complete",
            "",
            f"Samples matching 3+ opcodes: {three_plus}",
        ],
        "delay": 1000,
    }
    
    # Part 2: Determine mapping
    yield {
        "type": "text",
        "lines": [
            "Part 2: Determining opcode mapping...",
            "",
            "Using constraint propagation...",
        ],
        "delay": 500,
    }
    
    mapping = determine_opcode_mapping(samples)
    
    # Show some of the mapping
    op_names = {op: op.__name__ for op in ALL_OPS}
    mapping_lines = ["Opcode Mapping (sample):"]
    for opcode_num in sorted(mapping.keys())[:8]:
        mapping_lines.append(f"  {opcode_num}: {op_names[mapping[opcode_num]]}")
    mapping_lines.append("  ...")
    
    yield {
        "type": "text",
        "lines": mapping_lines,
        "delay": 1000,
    }
    
    # Execute program with animation
    yield {
        "type": "text",
        "lines": [
            "Executing test program...",
            "",
            "Registers: [0, 0, 0, 0]",
        ],
        "delay": 500,
    }
    
    regs = [0, 0, 0, 0]
    show_every = max(1, len(program) // 20)
    
    for i, instruction in enumerate(program):
        opcode_num, a, b, c = instruction
        mapping[opcode_num](regs, a, b, c)
        
        if i % show_every == 0 or i == len(program) - 1:
            yield {
                "type": "text",
                "lines": [
                    f"Instruction {i + 1}/{len(program)}",
                    f"  Opcode: {op_names[mapping[opcode_num]]}",
                    f"  Args: {a}, {b}, {c}",
                    f"  Registers: {regs}",
                ],
                "delay": 100,
            }
    
    yield {
        "type": "text",
        "lines": [
            "Program Complete!",
            "",
            f"Final register 0 value: {regs[0]}",
        ],
        "delay": 2000,
    }
