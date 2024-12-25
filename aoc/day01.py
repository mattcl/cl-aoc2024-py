"""01: Historian Hysteria"""
from collections import Counter

import aoc.util


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.left = []
        self.right = []

        for line in input.strip().split("\n"):
            parts = line.split("   ", maxsplit=1)
            self.left.append(int(parts[0]))
            self.right.append(int(parts[1]))

        self.left.sort()
        self.right.sort()
        self.counts = Counter(self.right)

    def part_one(self) -> int:
        return sum(abs(lv - rv) for lv, rv in zip(self.left, self.right))

    def part_two(self) -> int:
        return sum(v * self.counts[v] for v in self.left)
