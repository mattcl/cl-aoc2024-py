"""20: race condition"""
from multiprocessing import Pool

import aoc.util

SHORTCUT = 100

DIRS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        grid = list(list(line) for line in input.strip().split("\n"))

        height = len(grid)
        width = len(grid[0])

        cur = get_start(grid, width, height)

        path = []

        while True:
            path.append(cur)
            r, c = cur

            v = grid[r][c]

            if v == 'E':
                break

            grid[r][c] = '#'

            for dr, dc in DIRS:
                nr = r + dr
                nc = c + dc

                # we don't have to check if it's in the grid because the input
                # grid has a wall around it
                if grid[nr][nc] != '#':
                    cur = (nr, nc)
                    break

        self.p1 = 0
        self.p2 = 0

        with Pool(initializer=pool_init, initargs=[path]) as pool:
            for a, b in pool.map(search, range(len(path) - 1)):
                self.p1 += a
                self.p2 += b

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


def get_start(grid, width, height) -> (int, int):
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if grid[r][c] == 'S':
                return (r, c)


def pool_init(shared_path):
    global path
    global path_len
    path_len = len(shared_path)
    path = shared_path


def search(i: int) -> (int, int):
    global path
    global path_len
    p1 = 0
    p2 = 0

    ir, ic = path[i]

    j = i + SHORTCUT
    while j < path_len:
        jr, jc = path[j]

        dist = abs(jr - ir) + abs(jc - ic)

        if dist < 21 and j - i - dist >= SHORTCUT:
            if dist == 2:
                p1 += 1

            p2 += 1
        elif dist > 20:
            # we can jump ahead by at least this much
            j += dist - 20
            continue

        j += 1

    return (p1, p2)
