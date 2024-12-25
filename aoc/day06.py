"""06: guard gallivant"""
from multiprocessing import Pool

import aoc.util


NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

DELTAS = [(-1, 0), (1, 0), (0, 1), (0, -1)]
RIGHT = [EAST, WEST, SOUTH, NORTH]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.grid = []

        guard_found = False
        for r, line in enumerate(input.strip().split("\n")):
            self.grid.append(line)
            if not guard_found:
                for c, ch in enumerate(line):
                    if ch == '^':
                        self.guard_pos = (r, c)
                        guard_found = True
                        break

        self.size = len(self.grid)

        seen_locs = set()
        self.candidate_states = {}
        guard = (self.guard_pos[0], self.guard_pos[1], NORTH)

        seen_locs.add((guard[0], guard[1]))

        while True:
            r, c, dir = guard
            dr, dc = DELTAS[dir]

            nr = r + dr
            nc = c + dc

            if nr < 0 or nr >= self.size or nc < 0 or nc >= self.size:
                break

            ch = self.grid[nr][nc]
            if ch == '#':
                guard = (r, c, RIGHT[dir])
            else:
                if not (nr, nc) in seen_locs:
                    self.candidate_states[guard] = (nr, nc)
                    seen_locs.add((nr, nc))
                guard = (nr, nc, dir)

        self.p1 = len(seen_locs)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        # brute force, now with more cores
        with Pool(initializer=pool_init, initargs=[self.grid]) as pool:
            return sum(pool.map(check_position, list((guard, obs) for guard, obs in self.candidate_states.items())))


# the grid is immutable, so just init every worker in the pool with it so we
# don't have to pass it every time
def pool_init(shared_grid):
    global grid
    global size
    global cached_jumps
    grid = shared_grid
    size = len(shared_grid)
    # each worker will have its own cache, so it'll be useful beyond an
    # individual checked position
    cached_jumps = {}


def check_position(args) -> int:
    global grid
    global size

    guard, pos_info = args
    obs_r, obs_c = pos_info

    seen = set()
    seen.add(guard)

    while True:
        r, c, dir = guard
        dr, dc = DELTAS[dir]
        # find the first obstruction in our path, we only need to check the
        # points where we would change directions
        #
        # if we don't find a point and we walk off the grid, this can't be a
        # loop
        #
        # my rust solution afforded finding this location in O(1) time, but we
        # have to iterate here
        sr = r
        sc = c
        key = (sr, sc, dir)
        # we can't rely on the jump cache if we're in the row or column where we
        # added the obstacle
        if r != obs_r and c != obs_c and key in cached_jumps:
            guard = cached_jumps[key]
            if guard[0] < 0:
                return 0
        else:
            while True:

                r += dr
                c += dc

                if r < 0 or r >= size or c < 0 or c >= size:
                    # signal that this jump is off the grid
                    cached_jumps[key] = (-10, -10, -10)
                    return 0

                if (r == obs_r and c == obs_c) or grid[r][c] == '#':
                    guard = (r - dr, c - dc, RIGHT[dir])

                    # we can't rely on the jump cache if we're in the row or
                    # column where we added the obstacle, so don't store it
                    if r != obs_r and c != obs_c:
                        cached_jumps[key] = guard
                    break

        # we have the same location and orientation again, we're in a loop
        if guard in seen:
            return 1

        seen.add(guard)
