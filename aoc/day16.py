"""16: reindeer maze"""
from collections import defaultdict
from heapq import heappop, heappush

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

OPPOSITE = [
    SOUTH,
    WEST,
    NORTH,
    EAST,
]

START = 0
END = 1

UNVISITED_COST = 10000000000


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        graph = Graph()
        grid = list(list(line) for line in input.strip().split("\n"))
        height = len(grid)
        width = len(grid[0])

        # mark the start and end locations as junctions
        grid[height - 2][1] = 'X'
        graph.insert(height - 2, 1)

        grid[1][width - 2] = 'X'
        graph.insert(1, width - 2)

        # find all the remaining junctions
        for r in range(1, height - 1):
            for c in range(1, width - 1):
                if grid[r][c] == '.':
                    # more than 2 open paths as neighbors?
                    count = 0
                    for (dr, dc) in DIRS:
                        nr = r + dr
                        nc = c + dc

                        if grid[nr][nc] != '#':
                            count += 1

                        if count > 2:
                            grid[r][c] = 'X'
                            graph.insert(r, c)
                            break

        # okay, now map all the edges for those junctions
        for i in range(len(graph.nodes)):
            bfs_junction(i, graph, grid)

        # okay, now let's try to prune some of the edges/nodes
        for i in range(2):
            for i in range(2, len(graph.nodes)):
                if len(graph.nodes[i].edges) < 2:
                    remove_single_edge_nodes(graph, i)
                    continue

                prune_multiple_paths_to_same(graph, i)

                if join_corridor(graph, i):
                    continue

        # find the min path value
        costs = [UNVISITED_COST] * len(graph.nodes)
        self.p1 = dijkstra_min(graph, costs)
        self.p2 = dijkstra_all(graph, self.p1, costs)

    def part_one(self) -> int:
        return self.p1

    def part_two(self) -> int:
        return self.p2


class Graph(object):
    def __init__(self):
        self.nodes = []
        self.node_idxs = {}

    def insert(self, r: int, c: int):
        idx = len(self.nodes)
        self.nodes.append(Node(r, c))
        self.node_idxs[(r, c)] = idx


class Node(object):
    def __init__(self, r: int, c: int):
        self.r = r
        self.c = c
        self.edges = []


class Edge(object):
    def __init__(
        self,
        to: int,
        fr: int,
        cost: int,
        dist: int,
        enter_dir: int,
        exit_dir: int,
    ):
        self.to = to
        self.fr = fr
        self.cost = cost
        self.dist = dist
        self.enter_dir = enter_dir
        self.exit_dir = exit_dir
        self.reset_unique_index()

    def reset_unique_index(self):
        self.unique_idx = min(self.to, self.fr) * 10000 + max(self.to, self.fr)


def bfs_junction(idx, graph, grid):
    sr = graph.nodes[idx].r
    sc = graph.nodes[idx].c

    cur = []

    for dir, (dr, dc) in enumerate(DIRS):
        nr = sr + dr
        nc = sc + dc

        if grid[nr][nc] == '.':
            cur.append((nr, nc, dir, dir, 0, 0))

    while len(cur) > 0:
        next = []

        for r, c, orig_facing, facing, cost, dist in cur:
            for dir, (dr, dc) in enumerate(DIRS):
                nr = r + dr
                nc = c + dc

                if nr == sr and nc == sc:
                    continue

                if grid[nr][nc] != '#' and OPPOSITE[facing] != dir:
                    next_cost = cost + 1
                    if facing != dir:
                        next_cost += 1000

                    if grid[nr][nc] == 'X':
                        # this must exist
                        other = graph.node_idxs[(nr, nc)]

                        graph.nodes[idx].edges.append(
                            Edge(
                                other,
                                idx,
                                next_cost,
                                dist + 1,
                                orig_facing,
                                dir
                            )
                        )
                        continue

                    next.append((nr, nc, orig_facing, dir, next_cost, dist + 1))
                    break

        cur = next


def remove_single_edge_nodes(graph, i):
    if len(graph.nodes[i].edges) == 1:
        to = graph.nodes[i].edges[0].to
        graph.nodes[to].edges = [edge for edge in graph.nodes[to].edges if edge.to != i]
        graph.nodes[i].edges = []
        remove_single_edge_nodes(graph, to)


def join_corridor(graph, i) -> bool:
    if len(graph.nodes[i].edges) == 2:
        left = graph.nodes[i].edges[0]
        right = graph.nodes[i].edges[1]

        # we want to join these edges, so we need to know how much
        # it costs to move through it
        if OPPOSITE[left.enter_dir] == right.enter_dir:
            traverse_cost = 1
        else:
            traverse_cost = 1001

        cost = left.cost + right.cost + traverse_cost

        # the new distance includes the junction we're removing
        dist = left.dist + right.dist + 1

        for e in graph.nodes[left.to].edges:
            if e.to == i:
                e.to = right.to
                e.exit_dir = right.exit_dir
                e.dist = dist
                e.cost = cost
                e.reset_unique_index()
                break

        for e in graph.nodes[right.to].edges:
            if e.to == i:
                e.to = left.to
                e.exit_dir = left.exit_dir
                e.dist = dist
                e.cost = cost
                e.reset_unique_index()
                break

        graph.nodes[i].edges = []

        return True

    return False


def prune_multiple_paths_to_same(graph, i):
    if len(graph.nodes[i].edges) > 2:
        for j in range(len(graph.nodes[i].edges)):
            for k in range(j + 1, len(graph.nodes[i].edges)):
                if graph.nodes[i].edges[j].to == graph.nodes[i].edges[k].to:
                    left = graph.nodes[i].edges[j]
                    right = graph.nodes[i].edges[k]

                    if left.cost < right.cost:
                        graph.nodes[i].edges = [e for c, e in enumerate(graph.nodes[i].edges) if c != k]
                        graph.nodes[right.to].edges = [e for e in graph.nodes[right.to].edges if e.to != i or e.exit_dir != OPPOSITE[right.enter_dir]]
                        return
                    elif right.cost < left.cost:
                        graph.nodes[i].edges = [e for c, e in enumerate(graph.nodes[i].edges) if c != j]
                        graph.nodes[left.to].edges = [e for e in graph.nodes[left.to].edges if e.to != i or e.exit_dir != OPPOSITE[left.enter_dir]]
                        return
                    else:
                        graph.nodes[i].edges[j].dist += right.dist
                        graph.nodes[i].edges = [e for c, e in enumerate(graph.nodes[i].edges) if c != k]
                        graph.nodes[right.to].edges = [e for e in graph.nodes[right.to].edges if e.to != i or e.exit_dir != OPPOSITE[right.enter_dir]]

                        for edge in graph.nodes[right.to].edges:
                            if edge.to == i and edge.exit_dir == OPPOSITE[left.enter_dir]:
                                edge.dist += right.dist
                                return
                        return


def dijkstra_min(graph: Graph, costs) -> int:
    # ndoes in the heap are
    # (cost, facing, node_idx)
    heap = [(0, EAST, 0)]

    # now find the path
    while len(heap) > 0:
        (cur_cost, facing, idx) = heappop(heap)

        if idx == END:
            return cur_cost

        if cur_cost > costs[idx]:
            continue

        for edge in graph.nodes[idx].edges:
            if OPPOSITE[edge.enter_dir] == facing:
                continue

            next_cost = cur_cost + edge.cost + 1
            if facing != edge.enter_dir:
                next_cost += 1000

            if costs[edge.to] >= next_cost:
                costs[edge.to] = next_cost
                heappush(heap, (next_cost, edge.exit_dir, edge.to))


def dijkstra_all(graph: Graph, min_path_cost, costs) -> int:
    # ndoes in the heap are
    # (cost, facing, node_idx, state_link)
    heap = [(0, EAST, 0, -1)]
    state_links = []
    unique_edges = set()
    junctions = set()

    total_dist = 0

    # now find the path
    while len(heap) > 0:
        (cur_cost, facing, idx, link) = heappop(heap)

        if cur_cost > min_path_cost:
            break

        if idx == END:
            cur_link = link
            while cur_link >= 0:
                edge = state_links[cur_link].edge
                if edge.unique_idx not in unique_edges:
                    unique_edges.add(edge.unique_idx)
                    total_dist += edge.dist
                    junctions.add(edge.to)
                    junctions.add(edge.fr)
                cur_link = state_links[cur_link].prev

            continue

        for edge in graph.nodes[idx].edges:
            if OPPOSITE[edge.enter_dir] == facing:
                continue

            next_cost = cur_cost + edge.cost + 1
            if facing != edge.enter_dir:
                next_cost += 1000

            if costs[edge.to] + 1000 < next_cost:
                continue

            if costs[edge.to] == UNVISITED_COST:
                costs[edge.to] = next_cost

            next_link_idx = len(state_links)
            state_links.append(StateLink(edge, link))

            heappush(heap, (next_cost, edge.exit_dir, edge.to, next_link_idx))

    return total_dist + len(junctions)


class StateLink(object):
    def __init__(self, edge, prev):
        self.edge = edge
        self.prev = prev
