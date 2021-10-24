#!/usr/bin/env python
# coding: utf-8
"""
Navigating a Large Hexagon map on a Sphere.

We will build a map with a size of 4 hexagons between the 'poles'
"""

from copy import copy
from turtle import Turtle, VECTORS
from hex_map import empty_map
from hex_map_construct import perimeter, fill_centre, set_virtual, STEPS
from hex_map_construct import (
    EMPTY, COMMON, POLE, PENTAGON, VIRTUAL, EDGE, VERBOTEN, WRAP
)


def build_the_world():
    """Make a world and a turtle and put the turtle on it."""
    world = empty_map(STEPS * 12)
    turtle = Turtle(world)
    turtle.place(2, (STEPS + 1) * 6)
    perimeter(turtle)
    fill_centre(world)
    set_virtual(world)
    return turtle


def move(turtle):
    """Move the turtle from the WRAP node."""
    if turtle.state(COMMON):
        print("COMMON")
        turtle = from_common(turtle)
    if turtle.state(POLE):
        print("POLE")
        turtle = from_pole(turtle)
    if turtle.state(PENTAGON):
        print("PENTAGON")
        turtle = from_pentagon(turtle)
    if turtle.state(EDGE):
        print("EDGE")
        turtle = from_edge(turtle)
    if turtle.state(WRAP):
        print("WRAP")
        turtle = from_wrap(turtle)
    return turtle


def from_common(turtle):
    """Move the turtle from the COMMON node."""
    pass


def from_pole(turtle):
    """Move the turtle from the POLE node."""
    pass


def from_pentagon(turtle):
    """Move the turtle from the PENTAGON node."""
    pass


def from_edge(turtle):
    """Move the turtle from the EDGE node."""
    pass


def from_wrap(turtle):
    """Move the turtle from the WRAP node."""
    newt = copy(turtle)
    newt.move()
    if newt.state(COMMON):
        print("COMMON")
        turtle.move()
    else:
        print("Not COMMON")
        turtle = _from_wrap_to_virtual(turtle)
    return turtle


def _from_wrap_to_virtual(turtle):
    vurtle = copy(turtle)
    for x in range(turtle.x, len(turtle.bitmap[0]), 2):
        if turtle.bitmap[x, turtle.y] == WRAP:
            vurtle.x = x
    newt = copy(vurtle)
    newt.move()
    if newt.state(COMMON):
        print("Virtual COMMON")
        turtle = copy(newt)
    else:
        print("Virtual Not COMMON")
        turtle = _from_wrap_to_virtual_edge(turtle, vurtle)
    return turtle


def _from_wrap_to_virtual_edge(turtle, vurtle):
    newt = copy(turtle)
    newt.left()
    newt.move()
    if newt.state(COMMON):
        print("Left COMMON")
        turtle = copy(newt)
    else:
        print("Not Left COMMON")
        newt = copy(vurtle)
        newt.left()
        newt.move()
        if newt.state(COMMON):
            print("Virtual Left COMMON")
            turtle = copy(newt)
        else:
            print("Should Not Happen")
            raise Exception
    return turtle
