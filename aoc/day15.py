"""15: warehouse woes"""

import aoc.util

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DIRS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        parts = input.strip().split("\n\n")

        self.grid = list(list(line) for line in parts[0].split("\n"))
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.wide_width = self.width * 2

        self.wide_grid = [['.'] * self.wide_width for _ in range(len(self.grid))]
        self.instructions = list(
            map(
                int,
                (ch for ch in parts[1].replace("\n", "").replace(">", "1").replace("<", "3").replace("^", "0").replace("v", "2"))
            )
        )

        for r in range(self.height):
            for c in range(self.width):
                c_actual = c * 2

                match self.grid[r][c]:
                    case '#':
                        self.wide_grid[r][c_actual] = '#'
                        self.wide_grid[r][c_actual + 1] = '#'
                    case '@':
                        self.start = (r, c)
                        self.grid[r][c] = '.'
                    case 'O':
                        self.wide_grid[r][c_actual] = '['
                        self.wide_grid[r][c_actual + 1] = ']'

    def part_one(self) -> int:
        r, c = self.start
        for instruction in self.instructions:
            res = self.push_boxes(r, c, instruction)
            if res is not None:
                r, c = res

        out = 0
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                if self.grid[r][c] == 'O':
                    out += r * 100 + c

        return out

    def part_two(self) -> int:
        r, c = self.start
        c *= 2
        for instruction in self.instructions:
            res = self.push_wide_boxes(r, c, instruction)
            if res is not None:
                r, c = res

        out = 0
        for r in range(1, self.height - 1):
            for c in range(2, self.wide_width - 2):
                if self.wide_grid[r][c] == '[':
                    out += r * 100 + c

        return out

    def push_boxes(self, r, c, dir) -> (int, int):
        dr, dc = DIRS[dir]
        nr = dr + r
        nc = dc + c

        # we have pading int he grid from the input, so we're not even going to
        # check grid bounds
        nv = self.grid[nr][nc]

        match nv:
            case '.':
                return (nr, nc)
            case 'O':
                res = self.attempt_push(nr, nc, dir)
                if res is None:
                    return None
                lr, lc = res
                self.grid[lr][lc] = 'O'
                self.grid[nr][nc] = '.'
                return (nr, nc)
            case _:
                return None

    def attempt_push(self, r, c, dir) -> (int, int):
        dr, dc = DIRS[dir]
        nr = dr + r
        nc = dc + c

        nv = self.grid[nr][nc]

        match nv:
            case '.':
                return (nr, nc)
            case 'O':
                return self.attempt_push(nr, nc, dir)
            case _:
                return None

    def push_wide_boxes(self, r, c, dir) -> (int, int):
        dr, dc = DIRS[dir]
        nr = dr + r
        nc = dc + c

        nv = self.wide_grid[nr][nc]

        match nv:
            case '.':
                return (nr, nc)
            case '[':
                match dir:
                    case 0:
                        seen = set()
                        seen.add((nr, nc))
                        if self.push_north((nr, nc), (nr, nc + 1), seen):
                            seen = list(seen)
                            seen.sort()
                            for s in seen:
                                sr, sc = s
                                self.wide_grid[sr - 1][sc] = '['
                                self.wide_grid[sr - 1][sc + 1] = ']'
                                self.wide_grid[sr][sc] = '.'
                                self.wide_grid[sr][sc + 1] = '.'
                            return (nr, nc)
                        return None
                    case 2:
                        seen = set()
                        seen.add((nr, nc))
                        if self.push_south((nr, nc), (nr, nc + 1), seen):
                            seen = list(seen)
                            seen.sort()
                            seen.reverse()
                            for s in seen:
                                sr, sc = s
                                self.wide_grid[sr + 1][sc] = '['
                                self.wide_grid[sr + 1][sc + 1] = ']'
                                self.wide_grid[sr][sc] = '.'
                                self.wide_grid[sr][sc + 1] = '.'
                            return (nr, nc)
                        return None
                    case 1:
                        seen = [(nr, nc)]
                        if self.push_east(nr, nc, seen):
                            for i in range(len(seen) - 1, -1, -1):
                                sr, sc = seen[i]
                                self.wide_grid[sr][sc + 1] = '['
                                self.wide_grid[sr][sc + 2] = ']'
                                if i == 0:
                                    self.wide_grid[sr][sc] = '.'
                            return (nr, nc)
                        return None
                    case _:
                        assert False, "unreachable"
            case ']':
                match dir:
                    case 0:
                        seen = set()
                        seen.add((nr, nc - 1))
                        if self.push_north((nr, nc - 1), (nr, nc), seen):
                            seen = list(seen)
                            seen.sort()
                            for s in seen:
                                sr, sc = s
                                self.wide_grid[sr - 1][sc] = '['
                                self.wide_grid[sr - 1][sc + 1] = ']'
                                self.wide_grid[sr][sc] = '.'
                                self.wide_grid[sr][sc + 1] = '.'
                            return (nr, nc)
                        return None
                    case 2:
                        seen = set()
                        seen.add((nr, nc - 1))
                        if self.push_south((nr, nc - 1), (nr, nc), seen):
                            seen = list(seen)
                            seen.sort()
                            seen.reverse()
                            for s in seen:
                                sr, sc = s
                                self.wide_grid[sr + 1][sc] = '['
                                self.wide_grid[sr + 1][sc + 1] = ']'
                                self.wide_grid[sr][sc] = '.'
                                self.wide_grid[sr][sc + 1] = '.'
                            return (nr, nc)
                        return None
                    case 3:
                        seen = [(nr, nc)]
                        if self.push_west(nr, nc, seen):
                            for i in range(len(seen) - 1, -1, -1):
                                sr, sc = seen[i]
                                self.wide_grid[sr][sc - 1] = ']'
                                self.wide_grid[sr][sc - 2] = '['
                                if i == 0:
                                    self.wide_grid[sr][sc] = '.'
                            return (nr, nc)
                        return None
                    case _:
                        assert False, "unreachable"
            case _:
                return None

    def push_north(self, left, right, seen) -> bool:
        n_left = (left[0] - 1, left[1])
        n_right = (right[0] - 1, right[1])
        nvl = self.wide_grid[n_left[0]][n_left[1]]
        nvr = self.wide_grid[n_right[0]][n_right[1]]

        match (nvl, nvr):
            case ('.', '.'):
                return True
            case ('[', ']'):
                seen.add(n_left)
                return self.push_north(n_left, n_right, seen)
            case ('.', '['):
                seen.add(n_right)
                return self.push_north(n_right, (n_right[0], n_right[1] + 1), seen)
            case (']', '.'):
                m_left = (n_left[0], n_left[1] - 1)
                seen.add(m_left)
                return self.push_north(m_left, n_left, seen)
            case (']', '['):
                m_left = (n_left[0], n_left[1] - 1)
                seen.add(m_left)
                seen.add(n_right)
                return self.push_north(m_left, n_left, seen) and self.push_north(n_right, (n_right[0], n_right[1] + 1), seen)
            case _:
                return False

    def push_south(self, left, right, seen) -> bool:
        n_left = (left[0] + 1, left[1])
        n_right = (right[0] + 1, right[1])
        nvl = self.wide_grid[n_left[0]][n_left[1]]
        nvr = self.wide_grid[n_right[0]][n_right[1]]

        match (nvl, nvr):
            case ('.', '.'):
                return True
            case ('[', ']'):
                seen.add(n_left)
                return self.push_south(n_left, n_right, seen)
            case ('.', '['):
                seen.add(n_right)
                return self.push_south(n_right, (n_right[0], n_right[1] + 1), seen)
            case (']', '.'):
                m_left = (n_left[0], n_left[1] - 1)
                seen.add(m_left)
                return self.push_south(m_left, n_left, seen)
            case (']', '['):
                m_left = (n_left[0], n_left[1] - 1)
                seen.add(m_left)
                seen.add(n_right)
                return self.push_south(m_left, n_left, seen) and self.push_south(n_right, (n_right[0], n_right[1] + 1), seen)
            case _:
                return False

    def push_east(self, r, c, seen) -> bool:
        dr, dc = DIRS[EAST]
        nr = dr + r
        nc = 2 * dc + c

        nv = self.wide_grid[nr][nc]
        match nv:
            case '.':
                return True
            case '[':
                seen.append((nr, nc))
                return self.push_east(nr, nc, seen)
            case _:
                return False

    def push_west(self, r, c, seen) -> bool:
        dr, dc = DIRS[WEST]
        nr = dr + r
        nc = 2 * dc + c

        nv = self.wide_grid[nr][nc]
        match nv:
            case '.':
                return True
            case ']':
                seen.append((nr, nc))
                return self.push_west(nr, nc, seen)
            case _:
                return False


