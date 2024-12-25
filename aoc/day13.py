"""13: claw contraption"""

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        self.p1 = 0
        self.p2 = 0

        for section in input.strip().split("\n\n"):
            lines = section.split("\n")
            parts = lines[0].replace("Button A: X+", "").replace(", Y+", " ").split(" ")
            ax = int(parts[0])
            ay = int(parts[1])

            parts = lines[1].replace("Button B: X+", "").replace(", Y+", " ").split(" ")
            bx = int(parts[0])
            by = int(parts[1])

            parts = lines[2].replace("Prize: X=", "").replace(", Y=", " ").split(" ")
            px = int(parts[0])
            py = int(parts[1])

            r = cost_small(ax, ay, bx, by, px, py)
            if r:
                self.p1 += r

            r = cost_large(ax, ay, bx, by, px, py)
            if r:
                self.p2 += r

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


# it's just a matrix equation with two functions and two unknowns
def cost_small(ax, ay, bx, by, px, py):
    det = ax * by - ay * bx
    if det == 0:
        return None

    n = px * by - py * bx
    m = ax * py - ay * px

    if n % det != 0 or m % det != 0:
        return None

    return n // det * 3 + m // det


def cost_large(ax, ay, bx, by, px, py):
    px += 10000000000000
    py += 10000000000000

    det = ax * by - ay * bx
    if det == 0:
        return None

    n = px * by - py * bx
    m = ax * py - ay * px

    if n % det != 0 or m % det != 0:
        return None

    return n // det * 3 + m // det
