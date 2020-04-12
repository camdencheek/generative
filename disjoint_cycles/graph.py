import networkx as nx
import numpy as np
import random
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.matching import is_perfect_matching
from networkx.algorithms.regular import simple_k_factor
from networkx.algorithms.cycles import find_cycle
from sympy import *
import itertools as it

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except:
            return False

    def __str__(self):
        return f"({self.m},{self.n})"

    def point(self):
        return (self.x, self.y)


def construct_graph(rows, cols):
    g = nx.Graph()
    g.add_nodes_from(Node(i,j) for i in range(rows) for j in range(cols))
    for node in g.nodes():
        for adj in adjacent(node, rows, cols):
            g.add_edge(node, adj, weight=random.randint(1,10))
    return g


def adjacent(node, rows, cols):
    for i in range(node.x-1,node.x+2):
        for j in range(node.y-1, node.y+2):
            if i >= 0 and i < rows and j >= 0 and j < cols:
                if i == node.x and j == node.y:
                    continue
                yield Node(i,j)

def node_cycles(g):
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
    node_cycles = [[edge[0] for edge in cycle] for cycle in cycles]
    return node_cycles

def cycle_cubic_interpolate_symbolic(cycle):
    t, p0, p1, p2, p3 = symbols("t p0 p1, p2 p3")
    b = (1 - 3*t + 3*t**2 - t**3)*p0 + (t - 2*t**2 + t**3) *p1 + (t**2 - t**3) * p2 + t**3*p3







def cycle_cubic_interpolate(cycle):
    coeff_x = np.zeros((2*len(cycle), 2*len(cycle)), dtype=float)
    coeff_y = np.zeros((2*len(cycle), 2*len(cycle)), dtype=float)
    const_x = np.zeros((2*len(cycle)), dtype=float)
    const_y = np.zeros((2*len(cycle)), dtype=float)
    for i in range(len(cycle)):
        ia = i
        ib = (i+1)%len(cycle)
        # layout [ x1_(n) x2_(n) x1_(n+1) x2_(n+1) ]
        coeff_x[ia*2,ia*2+1] = -3
        coeff_x[ia*2,ib*2] = -3
        const_x[ia*2] = -6*cycle[ib].x

        coeff_y[ia*2,ia*2+1] = -3
        coeff_y[ia*2,ib*2] = -3
        const_y[ia*2] = -6*cycle[ib].y

        coeff_x[ia*2+1,ia*2] = 6
        coeff_x[ia*2+1,ia*2+1] = -12
        coeff_x[ia*2+1,ib*2] = 12
        coeff_x[ia*2+1,ib*2+1] = -6

        coeff_y[ia*2+1,ia*2] = 6
        coeff_y[ia*2+1,ia*2+1] = -12
        coeff_y[ia*2+1,ib*2] = 12
        coeff_y[ia*2+1,ib*2+1] = -6

    x = np.linalg.solve(coeff_x, const_x)
    y = np.linalg.solve(coeff_y, const_y)

    segments = [[
                 (node.x,node.y),
                 (x[i*2],y[i*2]),
                 (x[i*2+1],y[i*2+1]),
                 (cycle[(i+1)%len(cycle)].x, cycle[(i+1)%len(cycle)].y)
                ] for (i, node) in enumerate(cycle)]

    return segments



def remove_intersections(g, w, h):
    for (i,j) in it.product(range(w-1), range(h-1)):
        n00 = Node(i,j)
        n01 = Node(i,j+1)
        n10 = Node(i+1,j)
        n11 = Node(i+1,j+1)

        if g.has_edge(n00,n11) and g.has_edge(n10,n01):
            g.remove_edge(n00,n11)
            g.remove_edge(n10,n01)
            if g.has_edge(n00,n01) or g.has_edge(n10,n11):
                g.add_edge(n00,n10)
                g.add_edge(n01,n11)
            else:
                g.add_edge(n00,n01)
                g.add_edge(n10,n11)




def get_graph(w, h):
    g = construct_graph(w, h)
    return simple_k_factor(g, 2)


if __name__ == "__main__":
    main()
