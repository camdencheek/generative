import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
from simple_k_factor import *
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.matching import is_perfect_matching
from networkx.algorithms.cycles import find_cycle

class Node:
    def __init__(self, m, n):
        self.m = m
        self.n = n

    def __hash__(self):
        return hash((self.m, self.n))

    def __eq__(self, other):
        try:
            return self.m == other.m and self.n == other.n
        except:
            return False
    def __str__(self):
        return f"({self.m},{self.n})"


def construct_graph(rows, cols):
    g = nx.Graph()
    g.add_nodes_from(Node(i,j) for i in range(rows) for j in range(cols))
    for node in g.nodes():
        for adj in adjacent(node, rows, cols):
            g.add_edge(node, adj)
    return g


def adjacent(node, rows, cols):
    for i in range(node.m-1,node.m+2):
        for j in range(node.n-1, node.n+2):
            if i >= 0 and i < rows and j >= 0 and j < cols:
                if i == node.m and j == node.n:
                    continue
                yield Node(i,j)

def cycles(g):
    unvisited_nodes = set(g.nodes)
    cycles = []
    while True:
        if len(unvisited_nodes) == 0:
            break
        start = unvisited_nodes.pop()
        cycle = find_cycle(g, source=start)
        for edge in cycle:
            unvisited_nodes.discard(edge[0])
        cycles.append(cycle)
    return cycles




def get_graph(w, h):
    g = construct_graph(w, h)
    # then this: https://en.wikipedia.org/wiki/Vertex_cycle_cover
    # key phrase "disjoint cycle cover" or "vertex-disjoint"
    # See An Algorithm for Computing Simple k-Factors
    # print("".join("[" + ",".join(str(y) for y in x) + "]\n" for x in nx.cycle_basis(g)))
    inflated, gadgets = construct_inflated(g, 2)
    matching = max_weight_matching(inflated, maxcardinality=True)
    if not is_perfect_matching(inflated, matching):
        raise("cannot construct perfect matching")

    inflated.remove_edges_from(inflated.edges())
    for edge in matching:
        inflated.add_edge(edge[0], edge[1])

    for gadget in gadgets:
        gadget.restore_original(inflated)
    return inflated


if __name__ == "__main__":
    main()
