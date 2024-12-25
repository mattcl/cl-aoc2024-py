"""19: linen layout"""
from multiprocessing import Pool

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        parts = input.strip().split("\n\n")

        patterns = set(parts[0].split(", "))

        self.p1 = 0
        self.p2 = 0

        with Pool(initializer=pool_init, initargs=[patterns]) as pool:
            for v in pool.map(par_count_possible, parts[1].split("\n")):
                if v > 0:
                    self.p1 += 1
                    self.p2 += v

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


# the set of patterns is immutable so init every worker with it so we don't
# have to pass it every time
def pool_init(shared_patterns):
    global patterns
    patterns = shared_patterns


def par_count_possible(input) -> int:
    # this is faster than functools @cache on my machine
    cache = {}
    return count_possible(input, cache)


def count_possible(input, cache) -> int:
    global patterns

    if input in cache:
        return cache[input]

    ways = 0

    if input in patterns:
        ways += 1

    for i in range(1, len(input)):
        if input[:i] in patterns:
            ways += count_possible(input[i:], cache)

    cache[input] = ways

    return ways
