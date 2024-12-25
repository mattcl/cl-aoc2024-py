"""18: ram run"""
from copy import copy
from collections import defaultdict
from heapq import heappop, heappush

import aoc.util

SIZE = 71

DIRS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        initial_val = (1 << (SIZE + 1)) | 1
        self.grid = [initial_val] * (SIZE + 2)
        # walls on top and bottom
        self.grid[0] = (1 << (SIZE + 2)) - 1
        self.grid[SIZE + 1] = (1 << (SIZE + 2)) - 1

        self.remaining = []

        for idx, line in enumerate(input.strip().split("\n")):
            parts = line.split(',')
            c = int(parts[0])
            r = int(parts[1])

            if idx >= 1024:
                self.remaining.append((c, r))
            else:
                self.grid[r + 1] |= 1 << (c + 1)

        self.p1 = dijkstra_min(self.grid)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        # okay, let's binary search through the rest of the configurations

        # regular copy is fine, since these are just integers
        cur_grid = copy(self.grid)
        left = 0
        right = len(self.remaining)

        while left < right:
            cur_idx = (left + right) // 2

            # catch the grid up to where we are
            for i in range(left, cur_idx + 1):
                c, r = self.remaining[i]
                cur_grid[r + 1] |= 1 << (c + 1)

            res = dijkstra_min(cur_grid)

            # we found a path
            if res is not None:
                left = cur_idx + 1
            else:
                right = cur_idx

                # reset the grid up to the left bound
                cur_grid = copy(self.grid)
                for i in range(0, left + 1):
                    c, r = self.remaining[i]
                    cur_grid[r + 1] |= 1 << (c + 1)

        c, r = self.remaining[left]
        return f"{c},{r}"


def dijkstra_min(grid):
    # ndoes in the heap are
    # (cost, row, col)
    heap = [(0, 1, 1)]

    def default_value():
        return 10000000

    costs = defaultdict(default_value)
    costs[(1, 1)] = 0

    # now find the path
    while len(heap) > 0:
        (cur_cost, r, c) = heappop(heap)

        if r == SIZE and c == SIZE:
            return cur_cost

        if cur_cost > costs[(r, c)]:
            continue

        for dr, dc in DIRS:
            nr = r + dr
            nc = c + dc

            if grid[nr] & (1 << nc) == 0:
                next_cost = cur_cost + 1
                if costs[(nr, nc)] > next_cost:
                    costs[(nr, nc)] = next_cost
                    heappush(heap, (next_cost, nr, nc))

    return None
