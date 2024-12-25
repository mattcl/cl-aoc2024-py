"""25: code chronicle"""

import aoc.util

LOCK_MASK = 0b11111


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        keys = []
        locks = []

        for group in input.strip().split("\n\n"):
            out = 0
            for line in group.split("\n"):
                for ch in line:
                    out <<= 1
                    if ch == '#':
                        out |= 1

            if LOCK_MASK & out == 0:
                locks.append(out)
            else:
                keys.append(out)

        self.p1 = 0

        for key in keys:
            for lock in locks:
                if key & lock == 0:
                    self.p1 += 1

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0
