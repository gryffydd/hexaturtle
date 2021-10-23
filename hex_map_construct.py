#!/usr/bin/env python
# coding: utf-8
"""
Constructing Large Hexagon maps on a Sphere.

This works by drawing the perimeter, filling the middle,
and optionally drawing virtual hexgons around the outside.

How do these hexagons map to a sphere

The blue hexagons are mapped to the hexagons on a football. The green hexagons
are in fact pentagons, so the edge attached to a yellow hexagon does not
exist in reality, The purple hexagons are the same location on the sphere,
but are also in fact the pentagons on the football. They are equivalent to
the green hexagons. The aqua hexagons are the "poles" of the sphere and
therefore equivalent and also pentagons. The red hexagons are not accessible.
The yellow hexagons should be mapped to another hexagon in the map.
"""

from turtle import VECTORS

"""5 Sections for the map, 5 steps along the egdes."""
SECTIONS = 5
STEPS = 5

"""These are various types of hexagon (or cell)."""
EMPTY = 0
COMMON = 1
POLE = 2
PENTAGON = 3
VIRTUAL = 4
EDGE = 5
VERBOTEN = 6
WRAP = 7


def edgewise(turtle, value=EDGE):
    """Traverse the edge toward the pole."""
    for s in range(STEPS):
        turtle.right()
        turtle.move()
        turtle.set_value(COMMON)
        turtle.left()
        turtle.move()
        turtle.set_value(value)


def pole(turtle):
    """Set the pole and the verboten cell 'off' map."""
    turtle.set_value(POLE)
    turtle.move()
    turtle.set_value(VERBOTEN)
    turtle.right(3)
    turtle.move()
    turtle.left()


def hemisphere(turtle):
    """Traverse the 5 sections and then equatorial edge on the map."""
    for s in range(SECTIONS):
        edgewise(turtle)
        pole(turtle)
        edgewise(turtle)
        turtle.set_value(PENTAGON)
        turtle.left(2)
    turtle.set_value(WRAP)
    turtle.right(2)
    edgewise(turtle, WRAP)
    turtle.right()


def perimeter(turtle):
    """Northern hemisphere, then southern hemisphere."""
    hemisphere(turtle)
    hemisphere(turtle)


def fill_centre(bitmap):
    """
    Fill the cells in the middle.

    Once the perimeter is drawn, fill the centre by marking those between
    the common (and pentagon) cells.
    """
    markers = (COMMON, PENTAGON)
    for x in range(bitmap.shape[0]):
        mark = False
        for y in range(x % 2, bitmap.shape[1], 2):
            if bitmap[x, y] in markers:
                mark = not mark
            else:
                if mark:
                    bitmap[x, y] = COMMON


def set_virtual(bitmap):
    """Northern hemisphere, then southern hemisphere."""
    markers = (COMMON, POLE, PENTAGON, EDGE, WRAP)
    for x in range(1, bitmap.shape[0] - 1):
        for y in range(2 + x % 2, bitmap.shape[1] - 2, 2):
            if bitmap[x, y] == 0:
                for n in VECTORS:
                    if bitmap[x + n[0], y + n[1]] in markers:
                        bitmap[x, y] = VIRTUAL
