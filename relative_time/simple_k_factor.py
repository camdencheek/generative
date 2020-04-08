import networkx as nx
import random

class Gadget:
    def __init__(self, g, node, k, d):
        self.k = k
        self.original_node = node

        namespace = hash(node)
        self.outer_vertices = [namespace + x + 1 for x in range(d)]
        self.inner_vertices = [namespace + x + d + 1 for x in range(d)]
        self.core_vertices = [namespace + x + 2*d + 1 for x in range(k)]

    def replace_original(self, g):
        neighbors = g.neighbors(self.original_node)
        g.remove_node(self.original_node)
        for (outer, inner, neighbor) in zip(self.outer_vertices, self.inner_vertices, neighbors):
            g.add_node(outer)
            g.add_node(inner)
            g.add_edge(outer, inner, weight=random.randint(1,10))
            g.add_edge(outer, neighbor, weight=random.randint(1,10))
        for core in self.core_vertices:
            g.add_node(core)
            for inner in self.inner_vertices:
                g.add_edge(core, inner, weight=random.randint(1,10))

    def restore_original(self, g):
        g.add_node(self.original_node)
        for outer in self.outer_vertices:
            for neighbor in g.neighbors(outer):
                if not neighbor in self.inner_vertices:
                    g.add_edge(self.original_node, neighbor)
        g.remove_nodes_from(self.outer_vertices)
        g.remove_nodes_from(self.inner_vertices)
        g.remove_nodes_from(self.core_vertices)

def construct_inflated(old_g, k):
    g = old_g.copy()
    gadgets = []
    for node in g.nodes():
        degree = g.degree(node)
        if degree < k:
            raise("node has degree less than k")
        gadget = Gadget(g, node, k, degree)
        gadgets.append(gadget)
    for gadget in gadgets:
        gadget.replace_original(g)
    return (g, gadgets)



