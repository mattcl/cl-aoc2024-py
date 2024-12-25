"""07: bridge repair"""
import math
from multiprocessing import Pool

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.p1 = 0
        self.p2 = 0

        args = map(lambda parts: (int(parts[0]), list(map(int, parts[1].split(' ')))), map(lambda line: line.split(": "), input.strip().split("\n")))

        with Pool() as pool:
            results = pool.map(combined_dfs, args)
            for a, b in results:
                self.p1 += a
                self.p2 += b

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


def combined_dfs(args) -> (int, int):
    target, values = args
    num_values = len(values)

    if _p1_dfs(num_values, values, target):
        return (target, target)

    if _p2_dfs(num_values, values, target):
        return (0, target)

    return (0, 0)


def _p1_dfs(remaining, values, head) -> bool:
    if remaining == 0:
        return head == 0

    if head < 0:
        return False

    idx = remaining - 1
    v = values[idx]

    if head % v == 0 and _p1_dfs(idx, values, head / v):
        return True

    return _p1_dfs(idx, values, head - v)


def _p2_dfs(remaining, values, head) -> bool:
    if remaining == 0:
        return head == 0

    if head < 0:
        return False

    idx = remaining - 1
    v = values[idx]

    if head % v == 0 and _p2_dfs(idx, values, head / v):
        return True

    width = int(math.log10(v)) + 1
    divisor = pow(10, width)
    if head % divisor == v and _p2_dfs(idx, values, head // divisor):
        return True

    return _p2_dfs(idx, values, head - v)
