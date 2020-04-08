#!/usr/bin/env python
"""Based on cairo-demo/X11/cairo-demo.c"""

import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from graph import *
import random





def draw(ctx):
    ctx.set_source_rgb(0, 0, 0)

    ctx.set_line_width(10)
    ctx.set_tolerance(0.1)

    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.save()
    g = get_graph(10, 10)
    for cycle in cycles(g):
        ctx.new_path()
        for edge in cycle:
            x = 100 * edge[1].m + 50
            y = 100 * edge[1].n + 50
            ctx.curve_to(x, y, x, y, x, y)
        ctx.close_path()
        ctx.stroke()

def main():
    random.seed(10)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1200, 1200)
    ctx = cairo.Context(surface)
    ctx.save()
    draw(ctx)
    ctx.save()
    surface.write_to_png("test.png")



if __name__ == '__main__':
    main()
