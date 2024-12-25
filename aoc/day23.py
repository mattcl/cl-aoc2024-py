"""23: lan party"""
from copy import copy
from itertools import combinations

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)
        self.graph = Graph()

        for line in input.strip().split("\n"):
            parts = line.split("-")
            self.graph.insert(parts[0], parts[1])

    def part_one(self) -> int:
        groups = set()

        for node in self.graph.nodes:
            if node.name.startswith("t"):
                for i in range(len(node.edges)):
                    i_edge = node.edges[i]

                    for j in range(i + 1, len(node.edges)):
                        j_edge = node.edges[j]

                        if j_edge in self.graph.nodes[i_edge].edge_map:
                            key = [node.idx, i_edge, j_edge]
                            key.sort()
                            groups.add((key[0], key[1], key[2]))

        return len(groups)

    def part_two(self) -> int:
        maximum = max_clique_exploit(self.graph)

        names = [str(self.graph.nodes[x].name) for x in maximum]
        names.sort()

        return ",".join(names)


def max_clique_exploit(graph):
    for node in graph.nodes:
        if len(node.edges) < 12:
            continue

        for edges in combinations(node.edges, 12):
            working = copy(node.edge_map)

            for e in edges:
                working &= graph.nodes[e].edge_map

                if len(working) < 13:
                    break

            if len(working) >= 13:
                return working


class Graph(object):
    def __init__(self):
        self.nodes = []
        self.mapping = {}

    def insert(self, left: str, right: str):
        if left not in self.mapping:
            idx = len(self.nodes)
            self.nodes.append(Node(idx, left))
            self.mapping[left] = idx

        if right not in self.mapping:
            idx = len(self.nodes)
            self.nodes.append(Node(idx, right))
            self.mapping[right] = idx

        left_idx = self.mapping[left]
        right_idx = self.mapping[right]

        self.nodes[left_idx].insert_edge(right_idx)
        self.nodes[right_idx].insert_edge(left_idx)


class Node(object):
    def __init__(self, idx: int, name: str):
        self.idx = idx
        self.name = name
        self.edge_map = {idx}
        self.edges = []

    def insert_edge(self, idx: int):
        if idx not in self.edge_map:
            self.edges.append(idx)
            self.edge_map.add(idx)
