#!/usr/bin/env python

import cairo
import draw
import random
import graph
from networkx.algorithms.regular import k_factor
import networkx as nx


def main():
    print("debug-grid-nodiag-10.svg")
    with cairo.SVGSurface("debug-grid-nodiag-10.svg", 1600, 800) as surface:
        random.seed(10)
        SIZE = 10
        ctx = cairo.Context(surface)
        ctx.scale(800 / (SIZE + 1), 800 / (SIZE + 1))
        ctx.transform(cairo.Matrix(1, 0, 0, -1))
        ctx.translate(0, -SIZE-1)

        # fill background
        ctx.new_path()
        ctx.rectangle(0, 0, 2*SIZE+1, SIZE+1)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()

        g = nx.grid_2d_graph(SIZE, SIZE)

        ctx.translate(1, 1)

        draw.draw_debug(ctx, g)

        ctx.translate(SIZE, 0)

        graph.assign_random_weights(g)
        g = k_factor(g, 2)
        graph.remove_intersections(g, SIZE, SIZE)
        draw.draw_smooth_interpolate(ctx, g)

    print("debug-grid-diag-10.svg")
    with cairo.SVGSurface("debug-grid-diag-10.svg", 1600, 800) as surface:
        random.seed(11)
        SIZE = 10
        ctx = cairo.Context(surface)
        ctx.scale(800 / (SIZE + 1), 800 / (SIZE + 1))
        ctx.transform(cairo.Matrix(1, 0, 0, -1))
        ctx.translate(0, -SIZE-1)

        # fill background
        ctx.new_path()
        ctx.rectangle(0, 0, 2*SIZE+1, SIZE+1)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()

        g = graph.graph_grid_with_diag(SIZE, SIZE)

        ctx.translate(1, 1)

        draw.draw_debug(ctx, g)

        ctx.translate(SIZE, 0)

        graph.assign_random_weights(g)
        g = k_factor(g, 2)
        graph.remove_intersections(g, SIZE, SIZE)
        draw.draw_smooth_interpolate(ctx, g)

    print("debug-tri-10.svg")
    with cairo.SVGSurface("debug-tri-10.svg", 1600, 800) as surface:
        random.seed(10)
        SIZE = 7
        ctx = cairo.Context(surface)
        ctx.save()
        ctx.scale(800 / SIZE, 800 / SIZE)
        ctx.transform(cairo.Matrix(1, 0, 0, -1))
        ctx.translate(0, -SIZE)

        # fill background
        ctx.new_path()
        ctx.rectangle(0, 0, 2*SIZE, SIZE)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()

        ctx.translate(0.5, 0.5)

        g = nx.triangular_lattice_graph(SIZE, SIZE+3, with_positions=True)
        graph.pos_attribute_to_node(g)
        draw.draw_debug(ctx, g)

        ctx.restore()
        ctx.translate(800, 0)
        ctx.scale(800 / SIZE, 800 / SIZE)
        ctx.transform(cairo.Matrix(1, 0, 0, -1))
        ctx.translate(0, -SIZE)
        ctx.translate(0.5, 0.5)

        graph.assign_random_weights(g)
        g = k_factor(g, 2)
        graph.remove_intersections(g, SIZE, SIZE)
        draw.draw_smooth_interpolate(ctx, g)

    print("diagonal-cycles-10.svg")
    with cairo.SVGSurface("diagonal-cycles-10.svg", 1600, 800) as surface:
        random.seed(11)
        SIZE = 10
        ctx = cairo.Context(surface)
        ctx.scale(800 / (SIZE + 1), 800 / (SIZE + 1))
        ctx.transform(cairo.Matrix(1, 0, 0, -1))
        ctx.translate(0, -SIZE-1)

        # fill background
        ctx.new_path()
        ctx.rectangle(0, 0, 2*SIZE+1, SIZE+1)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()

        g = graph.graph_grid_with_diag(SIZE, SIZE)
        graph.assign_random_weights(g)
        g = k_factor(g, 2)

        ctx.translate(1, 1)

        draw.draw_lines(ctx, g)

        ctx.translate(SIZE, 0)

        draw.draw_fill(ctx, g)

    name = "diagonal-cycles-no-intersect-10.svg"
    print(name)
    with cairo.SVGSurface(name, 1600, 800) as surface:
        random.seed(11)
        SIZE = 10
        ctx = cairo.Context(surface)
        ctx.scale(800 / (SIZE + 1), 800 / (SIZE + 1))
        ctx.transform(cairo.Matrix(1, 0, 0, -1))
        ctx.translate(0, -SIZE-1)

        # fill background
        ctx.new_path()
        ctx.rectangle(0, 0, 2*SIZE+1, SIZE+1)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()

        g = graph.graph_grid_with_diag(SIZE, SIZE)
        graph.assign_random_weights(g)
        g = k_factor(g, 2)
        graph.remove_intersections(g, SIZE, SIZE)

        ctx.translate(1, 1)

        draw.draw_lines(ctx, g)

        ctx.translate(SIZE, 0)

        draw.draw_fill(ctx, g)


if __name__ == '__main__':
    main()
