import networkx as nx
import numpy as np
import random
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.matching import is_perfect_matching
from networkx.algorithms.cycles import find_cycle
from sympy import *
import itertools as it
from itertools import product

# Create a diagonally connected grid graph
def graph_grid_with_diag(rows, cols):
    g = nx.Graph()
    for node in product(range(rows), range(cols)):
        g.add_node(node)
        for adj in adjacent_grid_with_diag(node, rows, cols):
            g.add_edge(node, adj)
    return g


def adjacent_grid_with_diag(node, rows, cols):
    for i in range(node[0]-1,node[0]+2):
        for j in range(node[1]-1, node[1]+2):
            if i >= 0 and i < rows and j >= 0 and j < cols:
                if i == node[0] and j == node[1]:
                    continue
                yield (i,j)

def assign_random_weights(g):
    for edge in g.edges:
        g.add_edge(edge[0], edge[1], weight=random.randint(1,10))


# List the cycles in a 2-factored graph
# We know every node is part of a cycle at this point, so we can
# just go to each node and follow it through its cycle
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
        const_x[ia*2] = -6*cycle[ib][0]

        coeff_y[ia*2,ia*2+1] = -3
        coeff_y[ia*2,ib*2] = -3
        const_y[ia*2] = -6*cycle[ib][1]

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

    segments = [[ node, (x[i*2], y[i*2]), (x[i*2+1], y[i*2+1]), cycle[(i+1)%len(cycle)] ]
                for (i, node) in enumerate(cycle) ]

    return segments



def remove_intersections(g, w, h):
    for (i,j) in it.product(range(w-1), range(h-1)):
        n00 = (i,j)
        n01 = (i,j+1)
        n10 = (i+1,j)
        n11 = (i+1,j+1)

        if g.has_edge(n00,n11) and g.has_edge(n10,n01):
            g.remove_edge(n00,n11)
            g.remove_edge(n10,n01)
            if g.has_edge(n00,n01) or g.has_edge(n10,n11):
                g.add_edge(n00,n10)
                g.add_edge(n01,n11)
            else:
                g.add_edge(n00,n01)
                g.add_edge(n10,n11)
