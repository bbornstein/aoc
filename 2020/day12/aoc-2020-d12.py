#!/usr/bin/env python3

# Advent of Code 2020, Day 12 (https://adventofcode.com/2020/day/12)
# Author: Ben Bornstein


import collections
import math


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def parse (line):
    """Parses line into an `(action, value)` pair."""
    return line[0], int(line[1:])


def rotate (x, y, deg, clockwise=False):
    """Rotates (`x`, `y`) cartesian coordinates `deg`rees counterclockwise
    (default) or clockwise.  Assumes `(x, y)` are integer coordinates and
    maintains (returns) integer coordinates (i.e. rounds).
    """
    t  = math.radians(360 - deg if clockwise else deg)
    rx = round( x * math.cos(t) - y * math.sin(t) )
    ry = round( x * math.sin(t) + y * math.cos(t) )
    return rx, ry


filename = 'aoc-2020-d12.txt'
steps    = list( lines(filename, parse) )


# Part 1
#
# Figure out where the navigation instructions lead.
#
# Q: What is the Manhattan distance between that location and the ship's
# starting position?
# A: Part 1: Manhattan(origin, ship): 319.

sx, sy   = 0, 0
heading  = collections.deque(['E', 'S', 'W', 'N'])
actions  = {
    'N': lambda act, val: (sx, sy + val, None),
    'S': lambda act, val: (sx, sy - val, None),
    'E': lambda act, val: (sx + val, sy, None),
    'W': lambda act, val: (sx - val, sy, None),
    'F': lambda act, val: (sx, sy, heading[0]),
    'L': lambda act, val: (sx, sy, heading.rotate( val // 90)),
    'R': lambda act, val: (sx, sy, heading.rotate(-val // 90))
}

for act, val in steps:
    while act is not None:
        sx, sy, act = actions[act](act, val)

print(f'Part 1: Manhattan(origin, ship): {abs(sx) + abs(sy)}.')


# Part 2
#
# Figure out where the navigation instructions actually lead.
#
# Q: What is the Manhattan distance between that location and the ship's
# starting position?
# A: Part 2: Manhattan(origin, ship): 50157.

sx, sy  =  0, 0
wx, wy  = 10, 1
actions = {
    'N': lambda act, val: (sx, sy, wx, wy + val),
    'S': lambda act, val: (sx, sy, wx, wy - val),
    'E': lambda act, val: (sx, sy, wx + val, wy),
    'W': lambda act, val: (sx, sy, wx - val, wy),
    'F': lambda act, val: (sx + (val * wx), sy + (val * wy), wx, wy),
    'L': lambda act, val: (sx, sy, *rotate(wx, wy, val)),
    'R': lambda act, val: (sx, sy, *rotate(wx, wy, val, clockwise=True))
}

for act,  val in steps:
    sx, sy, wx, wy = actions[act](act, val)

print(f'Part 2: Manhattan(origin, ship): {abs(sx) + abs(sy)}.')
