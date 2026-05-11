"""
Intcode Computer — shared across 2019 puzzles.

A virtual machine with position/immediate parameter modes, I/O, and jumps.
Opcodes:
  1  ADD   p[c] = p[a] + p[b]
  2  MUL   p[c] = p[a] * p[b]
  3  INP   p[a] = next input
  4  OUT   output p[a]
  5  JNZ   if p[a] != 0: pc = p[b]
  6  JZ    if p[a] == 0: pc = p[b]
  7  LT    p[c] = 1 if p[a] < p[b] else 0
  8  EQ    p[c] = 1 if p[a] == p[b] else 0
  99 HALT  stop execution

Parameter modes (encoded in opcode digits):
  0  position — parameter is a memory address
  1  immediate — parameter is a literal value
"""


class IntcodeComputer:
    """Intcode interpreter for the 2019 Advent of Code series."""

    def __init__(self, program, inputs=None):
        self.memory = list(program)
        self.pc = 0
        self.halted = False
        self.inputs = list(inputs) if inputs else []
        self.outputs = []

    @classmethod
    def from_string(cls, text, inputs=None):
        """Parse a comma-separated program string."""
        return cls([int(x) for x in text.strip().split(",")], inputs)

    def reset(self, program):
        """Reset state with a fresh program."""
        self.memory = list(program)
        self.pc = 0
        self.halted = False
        self.inputs = []
        self.outputs = []

    def add_input(self, value):
        """Queue an input value."""
        self.inputs.append(value)

    def _read(self, param, mode):
        """Read a parameter value according to its mode."""
        if mode == 0:
            return self.memory[param]
        elif mode == 1:
            return param
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def run(self):
        """Execute until halt. Returns self for chaining."""
        while not self.halted:
            self.step()
        return self

    def step(self):
        """Execute a single instruction. Returns False when halted."""
        if self.halted or self.pc >= len(self.memory):
            self.halted = True
            return False

        instruction = self.memory[self.pc]
        op = instruction % 100
        modes = [(instruction // 10 ** (i + 2)) % 10 for i in range(3)]

        if op == 99:
            self.halted = True
            return False

        elif op == 1:  # ADD
            a = self._read(self.memory[self.pc + 1], modes[0])
            b = self._read(self.memory[self.pc + 2], modes[1])
            self.memory[self.memory[self.pc + 3]] = a + b
            self.pc += 4

        elif op == 2:  # MUL
            a = self._read(self.memory[self.pc + 1], modes[0])
            b = self._read(self.memory[self.pc + 2], modes[1])
            self.memory[self.memory[self.pc + 3]] = a * b
            self.pc += 4

        elif op == 3:  # INP
            self.memory[self.memory[self.pc + 1]] = self.inputs.pop(0)
            self.pc += 2

        elif op == 4:  # OUT
            self.outputs.append(self._read(self.memory[self.pc + 1], modes[0]))
            self.pc += 2

        elif op == 5:  # JNZ
            a = self._read(self.memory[self.pc + 1], modes[0])
            b = self._read(self.memory[self.pc + 2], modes[1])
            self.pc = b if a != 0 else self.pc + 3

        elif op == 6:  # JZ
            a = self._read(self.memory[self.pc + 1], modes[0])
            b = self._read(self.memory[self.pc + 2], modes[1])
            self.pc = b if a == 0 else self.pc + 3

        elif op == 7:  # LT
            a = self._read(self.memory[self.pc + 1], modes[0])
            b = self._read(self.memory[self.pc + 2], modes[1])
            self.memory[self.memory[self.pc + 3]] = 1 if a < b else 0
            self.pc += 4

        elif op == 8:  # EQ
            a = self._read(self.memory[self.pc + 1], modes[0])
            b = self._read(self.memory[self.pc + 2], modes[1])
            self.memory[self.memory[self.pc + 3]] = 1 if a == b else 0
            self.pc += 4

        else:
            raise ValueError(f"Unknown opcode {op} at position {self.pc}")

        return True
