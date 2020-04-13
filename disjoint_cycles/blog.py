#!/usr/bin/env python
"""Based on cairo-demo/X11/cairo-demo.c"""

from draw import *

def main():
    print("debug-grid-nodiag-10.svg")
    with cairo.SVGSurface("debug-grid-nodiag-10.svg", 1600, 800) as surface:
        random.seed(10)
        SIZE = 10
        ctx = cairo.Context(surface)
        ctx.scale(800 / (SIZE + 1), 800 / (SIZE + 1))
        ctx.transform(cairo.Matrix(1,0,0,-1))
        ctx.translate(0, -SIZE-1)

        # fill background
        ctx.new_path()
        ctx.rectangle(0,0, SIZE+1, SIZE+1)
        ctx.set_source_rgb(1,1,1)
        ctx.fill()

        g = grid_2d_graph(SIZE, SIZE)

        ctx.translate(1, 1)

        draw_debug(ctx, g)

        ctx.translate(SIZE, 0)

        assign_random_weights(g)
        g = simple_k_factor(g, 2)
        remove_intersections(g, SIZE, SIZE)
        draw_smooth_interpolate(ctx, g)

    print("debug-grid-diag-10.svg")
    with cairo.SVGSurface("debug-grid-diag-10.svg", 1600, 800) as surface:
        random.seed(11)
        SIZE = 10
        ctx = cairo.Context(surface)
        ctx.scale(800 / (SIZE + 1), 800 / (SIZE + 1))
        ctx.transform(cairo.Matrix(1,0,0,-1))
        ctx.translate(0, -SIZE-1)

        # fill background
        ctx.new_path()
        ctx.rectangle(0,0, SIZE+1, SIZE+1)
        ctx.set_source_rgb(1,1,1)
        ctx.fill()

        g = graph_grid_with_diag(SIZE, SIZE)

        ctx.translate(1, 1)

        draw_debug(ctx, g)

        ctx.translate(SIZE, 0)

        assign_random_weights(g)
        g = simple_k_factor(g, 2)
        remove_intersections(g, SIZE, SIZE)
        draw_smooth_interpolate(ctx, g)

    print("debug-tri-10.svg")
    with cairo.SVGSurface("debug-tri-10.svg", 1600, 800) as surface:
        random.seed(10)
        SIZE = 7
        ctx = cairo.Context(surface)
        ctx.save()
        ctx.scale(800 / SIZE, 800 / SIZE)
        ctx.transform(cairo.Matrix(1,0,0,-1))
        ctx.translate(0, -SIZE)

        # fill background
        ctx.new_path()
        ctx.rectangle(0,0, SIZE, SIZE)
        ctx.set_source_rgb(1,1,1)
        ctx.fill()

        ctx.translate(0.5, 0.5)


        g = triangular_lattice_graph(SIZE, SIZE+3, with_positions=True)
        pos_attribute_to_node(g)
        draw_debug(ctx, g)

        ctx.restore()
        ctx.translate(800, 0)
        ctx.scale(800 / SIZE, 800 / SIZE)
        ctx.transform(cairo.Matrix(1,0,0,-1))
        ctx.translate(0, -SIZE)
        ctx.translate(0.5, 0.5)

        assign_random_weights(g)
        g = simple_k_factor(g, 2)
        remove_intersections(g, SIZE, SIZE)
        draw_smooth_interpolate(ctx, g)

if __name__ == '__main__':
    main()
