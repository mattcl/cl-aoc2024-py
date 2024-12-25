"""11: plutonium pebbles"""
from collections import defaultdict
import math

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        cur = defaultdict(lambda: 0)
        for v in input.strip().split(' '):
            cur[int(v)] = 1

        for i in range(75):
            if i == 25:
                self.p1 = sum(cur.values())

            next = defaultdict(lambda: 0)
            for k, v in cur.items():
                if k == 0:
                    next[1] += v
                else:
                    digits = int(math.log10(k)) + 1
                    if digits % 2 == 0:
                        divisor = pow(10, digits // 2)
                        next[k // divisor] += v
                        next[k % divisor] += v
                    else:
                        next[k * 2024] += v

            cur = next

        self.p2 = sum(cur.values())

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2
