"""22: monkey market"""
from collections import defaultdict
from functools import reduce
from multiprocessing import Pool

import aoc.util

# -9 Ob00000  0
# -8 Ob00001  1
# -7 Ob00010  2
# -6 Ob00011  3
# -5 Ob00100  4
# -4 Ob00101  5
# -3 Ob00110  6
# -2 Ob00111  7
# -1 Ob01000  8
#  0 Ob01001  9
#  1 Ob01010  10
#  2 Ob01011  11
#  3 Ob01100  12
#  4 Ob01101  13
#  5 Ob01110  14
#  6 Ob01111  15
#  7 Ob10000  16
#  8 Ob10001  17
#  9 Ob10010  18

# N % 16,777,216 is equal to N & MOD_MASK;
MOD_MASK = (1 << 24) - 1
SEQ_MASK = (1 << 20) - 1

# Under our encoding scheme, the max value is the following sequence
#           9     0     0     0
SEQ_MAX = 0b10010_01001_01001_01001
# and the minimum is
#          -9     0     0     0
SEQ_MIN = 0b00000_01001_01001_01001

SEQ_SIZE = SEQ_MAX + 1 - SEQ_MIN

DESIRED_CHUNKS = 8
UNSEEN = 1 << 22


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        initial_vals = list(map(int, input.strip().split("\n")))

        groups = list(make_groups(initial_vals, DESIRED_CHUNKS))

        self.p2 = 0
        with Pool() as pool:
            res = list(pool.imap_unordered(compute, groups))

            # this is faster than summing an iterator
            self.p1 = res[0][0] + res[1][0] + res[2][0] + res[3][0] + res[4][0] + res[5][0] + res[6][0] + res[7][0]

            for i in range(SEQ_SIZE):
                # this is faster than summing an iterator
                candiate = res[0][1][i] + res[1][1][i] + res[2][1][i] + res[3][1][i] + res[4][1][i] + res[5][1][i] + res[6][1][i] + res[7][1][i]
                self.p2 = max(self.p2, candiate)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


def default():
    return 0


def pool_init():
    global totals

    totals = defaultdict(default)


def compute(values):
    totals = [0] * SEQ_SIZE
    seen = [UNSEEN] * SEQ_SIZE

    num_total = 0

    for i, n in enumerate(values):
        cur = n
        key = 0
        prev = cur % 10

        for j in range(2000):
            cur = next_number(cur)
            cur_digit = cur % 10
            delta = cur_digit - prev
            prev = cur_digit
            key = ((key << 5) & SEQ_MASK) | (delta + 9)

            adjusted_key = key - SEQ_MIN

            if j > 2 and seen[adjusted_key] != i:
                seen[adjusted_key] = i
                totals[adjusted_key] += cur_digit

        num_total += cur

    return [num_total, totals]


def next_number(input: int) -> int:
    a = input ^ (input << 6) & MOD_MASK
    a = a ^ (a >> 5)
    return a ^ ((a << 11) & MOD_MASK)


def make_groups(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def converge(acc, args):
    acc[0] += args[0]
    acc[1] = max(acc[1], args[1])

    for i in range(SEQ_SIZE):
        acc[2][i] += args[2][i]
        acc[1] = max(acc[1], acc[2][i])

    return acc
