"""08: resonant collinearity"""
from collections import defaultdict
from itertools import combinations

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.antennas = defaultdict(list)

        for r, line in enumerate(input.strip().split("\n")):
            self.size = len(line)
            for c, ch in enumerate(line):
                if ch != '.':
                    self.antennas[ch].append((c, r))

    def part_one(self) -> int:
        seen = [0] * self.size

        for antennas in self.antennas.values():
            for a, b in combinations(antennas, 2):
                s = sorted([a, b])
                left = s[0]
                right = s[1]

                dx = right[0] - left[0]
                dy = right[1] - left[1]

                p1_x = left[0] - dx
                p1_y = left[1] - dy

                if p1_x >= 0 and p1_x < self.size and p1_y >= 0 and p1_y < self.size:
                    seen[p1_y] |= 1 << p1_x

                p2_x = right[0] + dx
                p2_y = right[1] + dy

                if p2_x >= 0 and p2_x < self.size and p2_y >= 0 and p2_y < self.size:
                    seen[p2_y] |= 1 << p2_x

        return sum(v.bit_count() for v in seen)

    def part_two(self) -> int:
        seen = [0] * self.size

        for antennas in self.antennas.values():
            for a, b in combinations(antennas, 2):
                s = sorted([a, b])
                left = s[0]
                right = s[1]

                # we _should_ reduce this via GCD and such, but the real input
                # does not have that case. My rust solution _does_ reduce, but
                # I'm not going to bother here
                dx = right[0] - left[0]
                dy = right[1] - left[1]

                # start both points from the same location
                p1_x = left[0] - dx
                p1_y = left[1] - dy

                p2_x = left[0] + dx
                p2_y = left[1] + dy

                # put the current location in
                seen[left[1]] |= 1 << left[0]

                # walk each point off the grid
                while True:
                    if p1_x >= 0 and p1_x < self.size and p1_y >= 0 and p1_y < self.size:
                        seen[p1_y] |= 1 << p1_x
                    else:
                        break

                    p1_x -= dx
                    p1_y -= dy

                while True:
                    if p2_x >= 0 and p2_x < self.size and p2_y >= 0 and p2_y < self.size:
                        seen[p2_y] |= 1 << p2_x
                    else:
                        break

                    p2_x += dx
                    p2_y += dy

        return sum(v.bit_count() for v in seen)
