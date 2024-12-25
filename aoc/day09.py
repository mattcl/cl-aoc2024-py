"""09: disk fragmenter"""
import heapq
from itertools import batched

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        self.free_buckets = [[], [], [], [], [], [], [], [], [], []]
        # [(id, pos, size, free)]
        #   0    1    2      3
        self.files = []

        pos = 0

        for idx, chunk in enumerate(batched(input.strip(), 2)):
            if len(chunk) == 2:
                file = (idx, pos, int(chunk[0]), int(chunk[1]))
            else:
                file = (idx, pos, int(chunk[0]), 0)

            if file[3] > 0:
                self.free_buckets[file[3]].append(file[1] + file[2])

            self.files.append(file)

            pos += file[2] + file[3]

        # make binary heaps out of the nested vecs
        for i in range(1, 10):
            heapq.heapify(self.free_buckets[i])

    def part_one(self) -> int:
        checksum = 0

        # avoid mutating the actual lists at this point
        pos = 0
        head = 0
        tail = len(self.files) - 1
        rear = self.files[tail]

        while tail >= head:
            cur = rear if tail == head else self.files[head]

            checksum += checksum_file(cur, pos)

            pos += cur[2]

            free = cur[3]
            while free > 0 and tail > head:
                rear, taken = take(rear, free)

                checksum += rear[0] * (pos + pos + taken - 1) * taken // 2

                pos += taken
                free -= taken

                if rear[2] == 0:
                    tail -= 1
                    rear = self.files[tail]

            head += 1

        return checksum

    def part_two(self) -> int:
        checksum = 0

        for tail in range(len(self.files) - 1, -1, -1):
            cur = self.files[tail]

            min_bucket = -1
            min_pos = -1

            # find the left-most spot that will fit us
            for bucket_idx in range(cur[2], 10):
                if len(self.free_buckets[bucket_idx]) > 0:
                    candidate = self.free_buckets[bucket_idx][0]

                    if min_pos < 0 or candidate < min_pos:
                        min_pos = candidate
                        min_bucket = bucket_idx

            # is there a spot?
            if min_bucket > 0 and min_pos < cur[1]:
                free_pos = heapq.heappop(self.free_buckets[min_bucket])

                rem = min_bucket - cur[2]

                checksum += checksum_file(cur, free_pos)

                # update our buckets because we have rem free space
                if rem > 0:
                    heapq.heappush(self.free_buckets[rem], free_pos + cur[2])

            else:
                checksum += checksum_file(cur, cur[1])

        return checksum


def checksum_file(file, pos) -> int:
    return file[0] * (pos + pos + file[2] - 1) * file[2] // 2


# take amount blocks from the given file, returning a new file and the amount
# we were able to take
def take(file, amount) -> ((int, int, int, int), int):
    if amount > file[2]:
        return ((file[0], file[1], 0, file[3]), file[2])
    else:
        return ((file[0], file[1], file[2] - amount, file[3]), amount)
