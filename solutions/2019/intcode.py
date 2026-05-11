"""
Intcode Computer — shared across 2019 puzzles.

A simple virtual machine with position-addressed memory and a program counter.
Opcodes:
  1  ADD   mem[c] = mem[a] + mem[b]
  2  MUL   mem[c] = mem[a] * mem[b]
  99 HALT  stop execution
"""


class IntcodeComputer:
    """Intcode interpreter for the 2019 Advent of Code series."""

    def __init__(self, program):
        self.memory = list(program)
        self.pc = 0
        self.halted = False

    @classmethod
    def from_string(cls, text):
        """Parse a comma-separated program string."""
        return cls([int(x) for x in text.strip().split(",")])

    def reset(self, program):
        """Reset state with a fresh program."""
        self.memory = list(program)
        self.pc = 0
        self.halted = False

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

        op = self.memory[self.pc]

        if op == 99:
            self.halted = True
            return False
        elif op == 1:
            a, b, c = self.memory[self.pc + 1 : self.pc + 4]
            self.memory[c] = self.memory[a] + self.memory[b]
            self.pc += 4
        elif op == 2:
            a, b, c = self.memory[self.pc + 1 : self.pc + 4]
            self.memory[c] = self.memory[a] * self.memory[b]
            self.pc += 4
        else:
            raise ValueError(f"Unknown opcode {op} at position {self.pc}")

        return True