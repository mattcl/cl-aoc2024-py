"""03: Mull It Over"""

import aoc.util


# all solutions should subclass the `Solver` exposed by `aoc.util`
# this class MUST be called Solver for the CLI discovery to work
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

    # the bet here is that looping through the whole string twice will be faster
    # than using a regex lib. I had parser combinators via nom in rust, but we
    # have to use the builtins in python
    def part_one(self) -> int:
        input_len = len(self.input)
        start = 0
        sum = 0
        while start >= 0 and start < input_len:
            start = self.input.find("mul(", start)
            if start < 0 or start + 4 >= input_len:
                break

            start += 4

            # we want to look like mul(..,..)
            midpoint = self.input.find(",", start)

            if midpoint < 0 or midpoint == start or midpoint + 1 >= input_len:
                continue

            try:
                left = int(self.input[start:midpoint])
            except ValueError:
                continue

            closing = self.input.find(")", midpoint + 1)
            if closing < 0 or closing == midpoint + 1:
                continue

            try:
                right = int(self.input[(midpoint + 1):closing])
            except ValueError:
                continue

            start = closing + 1
            sum += left * right

        return sum

    def part_two(self) -> int:
        input_len = len(self.input)
        start = 0
        sum = 0
        while start >= 0 and start < input_len:
            dont = self.input.find("don't()", start)
            start = self.input.find("mul(", start)

            if dont >= 0 and dont < start:
                # we need to find the "do()"
                do = self.input.find("do()", dont)
                if do < 0:
                    break

                start = do
                continue

            if start < 0 or start + 4 >= input_len:
                break

            start += 4

            # we want to look like mul(..,..)
            midpoint = self.input.find(",", start)

            if midpoint < 0 or midpoint == start or midpoint + 1 >= input_len:
                continue

            try:
                left = int(self.input[start:midpoint])
            except ValueError:
                continue

            closing = self.input.find(")", midpoint + 1)
            if closing < 0 or closing == midpoint + 1:
                continue

            try:
                right = int(self.input[(midpoint + 1):closing])
            except ValueError:
                continue

            start = closing + 1
            sum += left * right

        return sum
