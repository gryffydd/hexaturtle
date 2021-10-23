#!/usr/bin/env python
# coding: utf-8
"""
Mapping Hexagons on a Sphere.

Square maps are great for tabletop games, but what about hexagons?

Hexagons are often used to simulate a space where things are more
equally spaced in every direction, but these are not easy to represent
in a computer array.  Not easy, but possible.

The second thing about hexagons is that you can use them to map a
space onto a sphere, like a football with a mix of hexagons and
12 pentagons.  The football has 20 hexagons and 12 pentagons,
but if you use more hexagons, you will always have 12 pentagons
like the points on a 20 sided dice.
(Icosahedron - https://en.wikipedia.org/wiki/Icosahedron)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from turtle import VECTORS


COLOURS = [
    "white", "blue", "cyan", "green", "yellow", "orange", "red", "purple"
]
X_SCALE = np.sqrt(3) / 2
Y_SCALE = 1 / 2


def thetas(sides=6):
    """Return an array of the angles for the points on a Polygon."""
    return [x / sides * 2 * np.pi for x in range(sides)]


def hexagon(x, y, r=1/np.sqrt(3)):
    """Return a Polygon that can be plotted with sides touching."""
    points = [[np.cos(t) * r + x, np.sin(t) * r + y] for t in thetas()]
    return Polygon(np.array(points))


def hexcolor(hex_type):
    """Return a Polygon that can be plotted with sides touching."""
    return COLOURS[hex_type % len(COLOURS)]


def empty_map(size=21):
    """Return a square array of zeros."""
    return np.zeros((size, size), dtype=np.int8)


def full_map(size=21, hex_type=1):
    """Return a square array of that represents a set of touching hexagons."""
    bitmap = empty_map(size=size)
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            if (x + y) % 2 == 0:
                bitmap[x, y] = hex_type
    return bitmap


def turtle_shape(turtle):
    """Return a Polygon that looks like an arrow pointing toward the facing."""
    points = (np.arange(0, 6, 2) + turtle.facing) % len(VECTORS)
    points = [VECTORS[p] for p in points]
    points.insert(2, [points[0][0] / 4.0, points[0][1] / 4.0])
    points = np.array(points, dtype=float)
    points *= np.array([X_SCALE, Y_SCALE]) / 3
    points += np.array([turtle.x * X_SCALE, turtle.y * Y_SCALE])
    return Polygon(points)


def add_hex_to_map(ax, bitmap, x, y):
    """Add a hexagon to the axes."""
    if bitmap[x, y] > 0:
        h = hexagon(x * X_SCALE, y * Y_SCALE)
        h.set_facecolor(hexcolor(bitmap[x, y]))
        h.set_edgecolor("black")
        h.set_alpha(0.4)
        ax.add_patch(h)


def local_map(turtle, horizon=3, add_turtle=True):
    """
    Plot the hexagons around the turtle using matplotlib.

    There are assumptions about the size of the hexagons and
    what bits are set in the array.
    """
    bitmap = turtle.bitmap
    fig, ax = plt.subplots()
    x_len, y_len = bitmap.shape
    x_min, x_max = turtle.x - horizon - 1, turtle.x + horizon + 1
    y_min, y_max = turtle.y - horizon - 1, turtle.y + horizon + 1
    for x in range(max(0, x_min), min(x_max, x_len)):
        for y in range(max(0, y_min), min(y_max, y_len)):
            add_hex_to_map(ax, bitmap, x, y)
    if add_turtle:
        ax.add_patch(turtle_shape(turtle))
    ax.set_xlim(xmin=(x_min * X_SCALE), xmax=(x_max * X_SCALE))
    ax.set_ylim(ymin=((y_min - 1) * Y_SCALE), ymax=((y_max + 1) * Y_SCALE))
    plt.show()


def world_map(bitmap):
    """
    Plot all the hexagons using matplotlib.

    There are assumptions about the size of the hexagons and
    what bits are set in the array.
    """
    fig, ax = plt.subplots()
    x_len, y_len = bitmap.shape
    for x in range(x_len):
        for y in range(y_len):
            if bitmap[x, y] > 0:
                add_hex_to_map(ax, bitmap, x, y)
    ax.set_xlim(xmax=(x_len*X_SCALE))
    ax.set_ylim(ymax=(y_len*Y_SCALE))
    plt.show()
