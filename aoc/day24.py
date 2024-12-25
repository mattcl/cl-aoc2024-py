"""24: crossed wires"""

import aoc.util


class Solver(aoc.util.Solver):
    def __init__(self, input: str):
        super(Solver, self).__init__(input)

        parts = input.strip().split("\n\n")

        self.graph = {}
        self.z_nodes = []

        for line in parts[0].split("\n"):
            initial_parts = line.split(": ")
            initial_parts[0]
            value = True if initial_parts[1] == '1' else False
            self.graph[initial_parts[0]] = Gate(initial_parts[0], value=value)

        for line in parts[1].split("\n"):
            gate_parts = line.split(" ")
            gate = Gate(
                gate_parts[4],
                left=gate_parts[0],
                right=gate_parts[2],
                op=gate_parts[1],
            )

            if gate.name.startswith("z"):
                self.z_nodes.append(gate.name)

            self.graph[gate.name] = gate

        self.z_nodes.sort()
        self.z_nodes.reverse()

    def part_one(self) -> int:
        out = 0
        for key in self.z_nodes:
            out <<= 1
            if self.graph[key].evaluate(self.graph):
                out |= 1

        return out

    def part_two(self) -> int:
        # this is cobbled together and appears to work generally enough for the
        # exptected inputs, but there's no official way to test that

        suspicious = set()

        origin_candidates = [v for v in self.graph.values() if v.is_origin() and v.op == "XOR"]

        for c in origin_candidates:
            if c.left == "x00" or c.right == "x00":
                if not c.name == "z00":
                    suspicious.add(c.name)
                continue
            elif c.name == "z00":
                suspicious.add(c.name)
                continue

            if c.name.startswith("z"):
                suspicious.add(c.name)

        output_candidates = [v for v in self.graph.values() if not v.is_origin() and v.op == "XOR"]

        for c in output_candidates:
            if not c.name.startswith("z"):
                suspicious.add(c.name)

        for c in (v for v in self.graph.values() if v.name.startswith("z")):
            if c.name == "z45":
                if c.op != "OR":
                    suspicious.add(c.name)
                continue
            elif c.op != "XOR":
                suspicious.add(c.name)

        additional = []

        for c in origin_candidates:
            if c.name in suspicious or c.name == "z00":
                continue

            if len([v for v in output_candidates if v.contains_input(c.name)]) == 0:
                suspicious.add(c.name)
                additional.append(c)

        for c in additional:
            key = f"z{c.left[1:]}"

            found = None
            for oc in output_candidates:
                if oc.name == key:
                    found = oc
                    break

            assert found is not None, "invalid input"

            or_gate = None
            for og in self.graph.values():
                if og.op == "OR" and (found.left == og.name or found.right == og.name):
                    or_gate = og
                    break

            if or_gate.name == found.left:
                suspicious.add(found.right)
            else:
                suspicious.add(found.left)

        assert len(suspicious) == 8, "could not solve input"

        out = list(suspicious)
        out.sort()

        return ",".join(out)


class Gate(object):
    def __init__(self, name: str, left=None, right=None, value=None, op=None):
        self.name = name
        self.left = left
        self.right = right
        self.value = value
        self.op = op

    def evaluate(self, graph) -> bool:
        if self.value is not None:
            return self.value

        match self.op:
            case "AND":
                return graph[self.left].evaluate(graph) and graph[self.right].evaluate(graph)
            case "OR":
                return graph[self.left].evaluate(graph) or graph[self.right].evaluate(graph)
            case "XOR":
                return graph[self.left].evaluate(graph) != graph[self.right].evaluate(graph)
            case _:
                assert False, "unreachable"

    def is_origin(self) -> bool:
        if self.left is None:
            return False

        return self.left.startswith("x") or self.right.startswith("x")

    def contains_input(self, input) -> bool:
        if self.left is None:
            return False

        return self.left == input or self.right == input
