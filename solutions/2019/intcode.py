"""
Intcode Computer — shared across 2019 puzzles.

A virtual machine with extensible memory, three parameter modes, and I/O.
Opcodes:
  1  ADD   p[c] = p[a] + p[b]
  2  MUL   p[c] = p[a] * p[b]
  3  INP   p[a] = next input
  4  OUT   output p[a]
  5  JNZ   if p[a] != 0: pc = p[b]
  6  JZ    if p[a] == 0: pc = p[b]
  7  LT    p[c] = 1 if p[a] < p[b] else 0
  8  EQ    p[c] = 1 if p[a] == p[b] else 0
  9  ARB   relative_base += p[a]
  99 HALT  stop execution

Parameter modes (encoded in opcode digits):
  0  position  — parameter is a memory address
  1  immediate — parameter is a literal value
  2  relative  — parameter is an offset from the relative base
"""


class IntcodeComputer:
    """Intcode interpreter for the 2019 Advent of Code series."""

    def __init__(self, program, inputs=None):
        self.memory = list(program)
        self.pc = 0
        self.relative_base = 0
        self.halted = False
        self.waiting_for_input = False
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
        self.relative_base = 0
        self.halted = False
        self.waiting_for_input = False
        self.inputs = []
        self.outputs = []

    def add_input(self, value):
        """Queue an input value. Clears waiting state if blocked."""
        self.inputs.append(value)
        self.waiting_for_input = False

    def _ensure(self, addr):
        """Extend memory with zeros if address is beyond current size."""
        if addr >= len(self.memory):
            self.memory.extend([0] * (addr - len(self.memory) + 1))

    def _get(self, addr):
        """Read memory at address, auto-extending if needed."""
        self._ensure(addr)
        return self.memory[addr]

    def _set(self, addr, value):
        """Write memory at address, auto-extending if needed."""
        self._ensure(addr)
        self.memory[addr] = value

    def _read(self, param, mode):
        """Read a parameter value according to its mode."""
        if mode == 0:
            return self._get(param)
        elif mode == 1:
            return param
        elif mode == 2:
            return self._get(self.relative_base + param)
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def _write_addr(self, param, mode):
        """Resolve the target address for a write parameter."""
        if mode == 0:
            return param
        elif mode == 2:
            return self.relative_base + param
        else:
            raise ValueError(f"Invalid write parameter mode {mode}")

    def run(self):
        """Execute until halt. Returns self for chaining."""
        while not self.halted:
            self.step()
        return self

    def run_until_block(self):
        """Execute until halt or waiting for input. Returns self."""
        self.waiting_for_input = False
        while not self.halted and not self.waiting_for_input:
            self.step()
        return self

    def step(self):
        """Execute a single instruction. Returns False when halted or blocked."""
        if self.halted or self.pc >= len(self.memory):
            self.halted = True
            return False

        instruction = self._get(self.pc)
        op = instruction % 100
        modes = [(instruction // 10 ** (i + 2)) % 10 for i in range(3)]

        if op == 99:
            self.halted = True
            return False

        elif op == 1:  # ADD
            a = self._read(self._get(self.pc + 1), modes[0])
            b = self._read(self._get(self.pc + 2), modes[1])
            self._set(self._write_addr(self._get(self.pc + 3), modes[2]), a + b)
            self.pc += 4

        elif op == 2:  # MUL
            a = self._read(self._get(self.pc + 1), modes[0])
            b = self._read(self._get(self.pc + 2), modes[1])
            self._set(self._write_addr(self._get(self.pc + 3), modes[2]), a * b)
            self.pc += 4

        elif op == 3:  # INP
            if not self.inputs:
                self.waiting_for_input = True
                return False
            self._set(self._write_addr(self._get(self.pc + 1), modes[0]), self.inputs.pop(0))
            self.pc += 2

        elif op == 4:  # OUT
            self.outputs.append(self._read(self._get(self.pc + 1), modes[0]))
            self.pc += 2

        elif op == 5:  # JNZ
            a = self._read(self._get(self.pc + 1), modes[0])
            b = self._read(self._get(self.pc + 2), modes[1])
            self.pc = b if a != 0 else self.pc + 3

        elif op == 6:  # JZ
            a = self._read(self._get(self.pc + 1), modes[0])
            b = self._read(self._get(self.pc + 2), modes[1])
            self.pc = b if a == 0 else self.pc + 3

        elif op == 7:  # LT
            a = self._read(self._get(self.pc + 1), modes[0])
            b = self._read(self._get(self.pc + 2), modes[1])
            self._set(self._write_addr(self._get(self.pc + 3), modes[2]), 1 if a < b else 0)
            self.pc += 4

        elif op == 8:  # EQ
            a = self._read(self._get(self.pc + 1), modes[0])
            b = self._read(self._get(self.pc + 2), modes[1])
            self._set(self._write_addr(self._get(self.pc + 3), modes[2]), 1 if a == b else 0)
            self.pc += 4

        elif op == 9:  # ARB (adjust relative base)
            self.relative_base += self._read(self._get(self.pc + 1), modes[0])
            self.pc += 2

        else:
            raise ValueError(f"Unknown opcode {op} at position {self.pc}")

        return True
