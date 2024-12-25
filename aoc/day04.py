"""04: Ceres Search"""

import aoc.util

# we don't have the neighbor-aware grid in my rust std, so this will have to do
EAST = [(0, 1, 'M'), (0, 2, 'A'), (0, 3, 'S')]
WEST = [(0, -1, 'M'), (0, -2, 'A'), (0, -3, 'S')]
NORTH = [(-1, 0, 'M'), (-2, 0, 'A'), (-3, 0, 'S')]
SOUTH = [(1, 0, 'M'), (2, 0, 'A'), (3, 0, 'S')]
NE = [(-1, 1, 'M'), (-2, 2, 'A'), (-3, 3, 'S')]
NW = [(-1, -1, 'M'), (-2, -2, 'A'), (-3, -3, 'S')]
SE = [(1, 1, 'M'), (2, 2, 'A'), (3, 3, 'S')]
SW = [(1, -1, 'M'), (2, -2, 'A'), (3, -3, 'S')]

DIRS = [NORTH, WEST, EAST, SOUTH, NE, SE, SW, NW]

CROSS = [
    ((1, 1), (-1, -1)),
    ((1, -1), (-1, 1)),
]


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.grid = list(input.strip().split("\n"))

    # this is going to be way slower than rust because of the array access and
    # offsets
    def part_one(self) -> int:
        size = len(self.grid)
        count = 0
        for r, line in enumerate(self.grid):
            for c, v in enumerate(line):
                if v == 'X':
                    for dir in DIRS:
                        for dr, dc, expected in dir:
                            nr = dr + r
                            nc = dc + c

                            if nr < 0 or nr >= size or nc < 0 or nc >= size:
                                break

                            if self.grid[nr][nc] == expected:
                                if expected == 'S':
                                    count += 1
                            else:
                                break

        return count

    def part_two(self) -> int:
        size = len(self.grid)
        count = 0
        for r, line in enumerate(self.grid):
            for c, v in enumerate(line):
                if v == 'A' and self.check_cross(size, r, c):
                    count += 1

        return count

    def check_cross(self, size, r, c) -> bool:
        arm1, arm2 = CROSS[0]
        nr = arm1[0] + r
        nc = arm1[1] + c

        if nr < 0 or nr >= size or nc < 0 or nc >= size:
            return False

        a = self.grid[nr][nc]

        nr = arm2[0] + r
        nc = arm2[1] + c

        if nr < 0 or nr >= size or nc < 0 or nc >= size:
            return False

        b = self.grid[nr][nc]
        if not ((a == 'M' and b == 'S') or (a == 'S' and b == 'M')):
            return False

        arm1, arm2 = CROSS[1]
        nr = arm1[0] + r
        nc = arm1[1] + c

        if nr < 0 or nr >= size or nc < 0 or nc >= size:
            return False

        a = self.grid[nr][nc]

        nr = arm2[0] + r
        nc = arm2[1] + c

        if nr < 0 or nr >= size or nc < 0 or nc >= size:
            return False

        b = self.grid[nr][nc]

        return (a == 'M' and b == 'S') or (a == 'S' and b == 'M')


