"""02: Red-Nosed Reports"""

import aoc.util


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        self.part1_count = 0
        self.part2_count = 0

        for line in input.strip().split("\n"):
            p1, p2 = _process(line)
            if p1:
                self.part1_count += 1

            if p2:
                self.part2_count += 1

    def part_one(self) -> int:
        return self.part1_count

    def part_two(self) -> int:
        return self.part2_count


def _process(line: str) -> (bool, bool):
    buffer = []
    vals = list(map(int, line.strip().split()))
    count = len(vals)

    first_candidate = [vals[0], 0, True]
    buffer.append([vals[1], 0, True])
    buffer.append(first_candidate.copy())
    _push(first_candidate, vals[1])

    for i in range(2, count):
        buffer = [elem for elem in buffer if _push(elem, vals[i])]

        if first_candidate[2]:
            buffer.append(first_candidate.copy())
        elif len(buffer) == 0:
            return (False, False)

        _push(first_candidate, vals[i])

    if first_candidate[2]:
        return (True, True)
    else:
        return (False, any(c[2] for c in buffer))


def _push(obj, val: int) -> bool:
    delta = obj[0] - val
    obj[0] = val

    if delta == 0 or abs(delta) > 3:
        obj[2] = False
        return False

    signum = 1 if delta > 0 else -1

    if obj[1] == 0:
        obj[1] = signum
        return True
    elif signum != obj[1]:
        obj[2] = False
        return False
    else:
        return True
