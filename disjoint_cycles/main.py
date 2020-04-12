#!/usr/bin/env python
"""Based on cairo-demo/X11/cairo-demo.c"""

import cairo
from graph import *
import random
import numpy.linalg as lin
import numpy as np
import itertools as it

def path_interpolated_cycle(ctx, cycle):
    segments = cycle_cubic_interpolate(cycle)
    ctx.move_to(segments[0][0][0], segments[0][0][1])
    for segment in segments:
        ctx.curve_to(segment[1][0], segment[1][1], segment[2][0], segment[2][1], segment[3][0], segment[3][1])


def path_tangent_cycle(ctx, cycle, smooth=0.3):
    start = cycle[1].point()
    ctx.move_to(start[0], start[1])
    for i in range(len(cycle)):
        a,b,c,d = cycle[i%len(cycle)].point(), cycle[(i+1)%len(cycle)].point(), cycle[(i+2)%len(cycle)].point(), cycle[(i+3)%len(cycle)].point()
        t1 = smooth * tangent_vector(a, b, c)
        t2 = smooth * tangent_vector(b, c, d)
        ctx.curve_to(b[0]+t1[0], b[1]+t1[1], c[0]-t2[0], c[1]-t2[1], c[0], c[1])

def path_straight(ctx, cycle):
    for node in cycle:
        x = node.x
        y = node.y
        ctx.line_to(x, y)

def draw_lines(ctx, g):
    ctx.set_source_rgb(0, 0, 0)

    ctx.set_line_width(0.1)
    ctx.set_tolerance(0.1)

    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for cycle in node_cycles(g):
        ctx.new_path()
        path_straight(ctx, cycle)
        ctx.close_path()
        ctx.stroke()

def draw_fill(ctx, g):
    ctx.set_source_rgb(0, 0, 0)

    ctx.set_line_width(0.1)
    ctx.set_tolerance(0.1)

    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for cycle in node_cycles(g):
        ctx.new_path()
        path_straight(ctx, cycle)
        ctx.close_path()
        ctx.fill()

def draw_smooth(ctx, g):
    ctx.set_source_rgb(0, 0, 0)

    ctx.set_line_width(0.05)
    ctx.set_tolerance(0.1)

    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for cycle in node_cycles(g):
        ctx.new_path()
        path_tangent_cycle(ctx, cycle)
        ctx.fill()

def draw_smooth_interpolate(ctx, g):
    ctx.set_source_rgba(0, 0, 0, 0.5)

    ctx.set_line_width(0.01)
    ctx.set_tolerance(0.1)

    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for cycle in node_cycles(g):
        ctx.new_path()
        path_interpolated_cycle(ctx, cycle)
        ctx.fill()

def tangent_vector(a, b, c):
    a = np.array([a[0],a[1],0], dtype=float)
    b = np.array([b[0],b[1],0], dtype=float)
    c = np.array([c[0],c[1],0], dtype=float)
    to_a = a - b
    to_c = c - b

    d_theta = np.arctan2(np.dot([0,0,1], np.cross(to_a, to_c)), np.dot(to_a, to_c))
    if d_theta < 0:
        d_theta += 2*np.pi
    theta_a = np.arctan2(to_a[1], to_a[0])
    theta = theta_a + d_theta / 2.
    tangent = np.array((np.cos(theta + np.pi / 2), np.sin(theta + np.pi / 2)))

    return tangent

def main():
    SIZE = 10
    random.seed(10)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1200, 1200)
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

    g = get_graph(SIZE, SIZE)
    remove_intersections(g, SIZE, SIZE)
    draw_smooth_interpolate(ctx, g)
    surface.write_to_png("test.png")

if __name__ == '__main__':
    main()
