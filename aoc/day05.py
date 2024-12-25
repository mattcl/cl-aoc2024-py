"""05: print queue"""

import aoc.util


# I was able to take advantage of the u128 support in rust to do this with
# bitmasks. We're going to attempt this in python, too
class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        # sets self.input to the provided input
        super(Solver, self).__init__(input)

        parts = input.strip().split("\n\n")

        self.rules_left = [0] * 100
        self.rules_right = [0] * 100

        for raw_rule in parts[0].split("\n"):
            rule_parts = raw_rule.split("|")
            left = int(rule_parts[0])
            right = int(rule_parts[1])

            self.rules_left[left] |= 1 << right
            self.rules_right[right] |= 1 << left

        self.updates = list(list(map(int, raw_update.split(","))) for raw_update in parts[1].split("\n"))

    def part_one(self) -> int:
        sum = 0
        for update in self.updates:
            if self._is_valid(update):
                sum += update[len(update) // 2]

        return sum

    def part_two(self) -> int:
        return sum(self._reorderd_middle(update) for update in self.updates if not self._is_valid(update))

    def _is_valid(self, update) -> bool:
        seen_before = 0
        for page in update:
            left = self.rules_left[page]

            # if our existing mask matches any of the numbers from the left rule
            # we know we're invalid
            if left != 0 and seen_before & left != 0:
                return False

            seen_before |= 1 << page

        return True

    # we don't need to actually re-order, we just need to know what the
    # reordered middle number _would_ be to compute the sum
    def _reorderd_middle(self, update) -> int:
        each_side = len(update) // 2

        seen = 0

        max = (1 << 128) - 1

        for page in update:
            seen |= 1 << page

        for page in update:
            cur = seen & (max - (1 << page))
            # check the number of numbers that need to be to our left
            rule = self.rules_left[page]
            if rule == 0 or (cur & rule).bit_count() != each_side:
                continue

            # check the number of numbers that need to be to our right
            rule = self.rules_right[page]
            if rule == 0 or (cur & rule).bit_count() != each_side:
                continue

            # if we're here, we have exactly each_side number to the left and
            # right, which is a necessary property for the correct value in
            # order for the problem to not be ambiguous
            return page

        # if it were possible to reach this line, the input wouldn't have a
        # single solution
        assert False, "unreachable"
