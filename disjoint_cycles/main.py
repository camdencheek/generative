#!/usr/bin/env python
"""Based on cairo-demo/X11/cairo-demo.c"""

import cairo
from graph import *
import random

def draw(ctx, w, h):
    ctx.set_source_rgb(0, 0, 0)

    ctx.set_line_width(0.1)
    ctx.set_tolerance(0.1)

    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.save()
    g = get_graph(w, h)
    for cycle in cycles(g):
        ctx.new_path()
        for edge in cycle:
            x = edge[1].m
            y = edge[1].n
            ctx.curve_to(x, y, x, y, x, y)
        ctx.close_path()
        ctx.fill()
        ctx.stroke()

def main():
    SIZE = 10
    # random.seed(10)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1200, 1200)
    ctx = cairo.Context(surface)
    ctx.scale(1200 / (SIZE + 1), 1200 / (SIZE + 1))

    # fill background
    ctx.new_path()
    ctx.rectangle(0,0, SIZE+1, SIZE+1)
    ctx.set_source_rgb(1,1,1)
    ctx.fill()
    ctx.save()

    ctx.translate(1, 1)
    ctx.save()

    draw(ctx, SIZE, SIZE)
    ctx.save()
    surface.write_to_png("test.png")

if __name__ == '__main__':
    main()
