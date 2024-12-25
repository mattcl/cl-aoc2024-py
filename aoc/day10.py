"""10: hoof it"""

import aoc.util


DIRS = [(-1, 0), (1, 0), (0, 1), (0, -1)]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        grid = [list(int(v) for v in line) for line in input.strip().split("\n")]

        height = len(grid)
        width = len(grid[0])

        self.p1 = 0
        self.p2 = 0

        cache = []
        for i in range(height):
            row = [None] * width
            cache.append(row)

        for r in range(height):
            for c in range(width):
                if grid[r][c] == 0:
                    unique, total = sum_trailheads(height, width, grid, (r, c), cache)
                    self.p1 += len(unique)
                    self.p2 += total

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


def sum_trailheads(height, width, grid, pos, cache):
    r, c = pos
    cur = grid[r][c]

    if cur == 9:
        return ({pos}, 1)

    if cache[r][c] is not None:
        return cache[r][c]

    out = set()
    total = 0

    for (dr, dc) in DIRS:
        nr = dr + r
        nc = dc + c

        if nr < 0 or nr >= height or nc < 0 or nc >= width:
            continue

        neighbor = grid[nr][nc]

        if cur + 1 == neighbor:
            unique, n_total = sum_trailheads(height, width, grid, (nr, nc), cache)
            out.update(unique)
            total += n_total

    cache[r][c] = (out, total)

    return (out, total)
