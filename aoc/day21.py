"""21: keypad conundrum"""
from functools import cache
from itertools import permutations

import aoc.util


DIGIT_HOLE = (0, 3)
NAV_HOLE = (0, 0)

DIGITS = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
}

NAV = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}

DIRS = {
    '^': (0, -1),
    '<': (-1, 0),
    'v': (0, 1),
    '>': (1, 0),
}


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        self.p1 = 0
        self.p2 = 0

        for line in input.strip().split("\n"):
            val = int(line[:3])
            self.p1 += val * min_path(line, 0, 2)
            self.p2 += val * min_path(line, 0, 25)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2

    def reset_caches():
        digit_paths.cache_clear()
        nav_paths.cache_clear()
        min_path.cache_clear()


def avoids_hole(path, start, hole) -> bool:
    x, y = start
    for p in path:
        dx, dy = DIRS[p]
        x += dx
        y += dy

        if x == hole[0] and y == hole[1]:
            return False

    return True


@cache
def digit_paths(fr, to):
    dx = to[0] - fr[0]
    dy = to[1] - fr[1]

    base = ""

    if dy < 0:
        base += '^' * abs(dy)
    elif dy > 0:
        base += 'v' * dy

    if dx < 0:
        base += '<' * abs(dx)
    elif dx > 0:
        base += '>' * dx

    if len(base) == 0:
        return ['A']

    out = list(x + 'A' for x in set(map("".join, permutations(base))) if avoids_hole(x, fr, DIGIT_HOLE))

    if len(out) == 0:
        return ['A']

    return out


@cache
def nav_paths(fr, to):
    dx = to[0] - fr[0]
    dy = to[1] - fr[1]

    base = ""

    if dy < 0:
        base += '^' * abs(dy)
    elif dy > 0:
        base += 'v' * dy

    if dx < 0:
        base += '<' * abs(dx)
    elif dx > 0:
        base += '>' * dx

    if len(base) == 0:
        return ['A']

    out = list(x + 'A' for x in set(map("".join, permutations(base))) if avoids_hole(x, fr, NAV_HOLE))

    if len(out) == 0:
        return ['A']

    return out


@cache
def min_path(seq, depth, max_depth) -> int:
    length = 0

    if depth == 0:
        cur = DIGITS['A']
        for ch in seq:
            next = DIGITS[ch]
            paths = digit_paths(cur, next)
            length += min(min_path(p, depth + 1, max_depth) for p in paths)
            cur = next
    else:
        cur = NAV['A']
        for ch in seq:
            next = NAV[ch]
            paths = nav_paths(cur, next)
            if depth == max_depth:
                length += len(paths[0])
            else:
                length += min(min_path(p, depth + 1, max_depth) for p in paths)
            cur = next

    return length
