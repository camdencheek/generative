#!/usr/bin/env python
"""Based on cairo-demo/X11/cairo-demo.c"""

import cairo
from graph import *
import random
from draw import *
from networkx.algorithms.regular import simple_k_factor

def main():
    SIZE = 15
    random.seed(10)
    with cairo.SVGSurface("20.svg", 1200, 1200) as surface:
        ctx = cairo.Context(surface)
        ctx.scale(1200 / (SIZE + 1), 1200 / (SIZE + 1))
        ctx.transform(cairo.Matrix(1,0,0,-1))
        ctx.translate(0, -SIZE-1)

        # fill background
        ctx.new_path()
        ctx.rectangle(0,0, SIZE+1, SIZE+1)
        ctx.set_source_rgb(1,1,1)
        ctx.fill()

        ctx.translate(1, 1)

        g = graph_grid_with_diag(SIZE, SIZE)
        assign_random_weights(g)
        g = simple_k_factor(g, 2)
        remove_intersections(g, SIZE, SIZE)
        draw_smooth_interpolate(ctx, g)

if __name__ == '__main__':
    main()
