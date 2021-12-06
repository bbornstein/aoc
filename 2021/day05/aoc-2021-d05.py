#!/usr/bin/env python3

# Advent of Code 2021, Day 5 (https://adventofcode.com/2021/day/5)
# Author: Ben Bornstein

import collections


Point = collections.namedtuple('Point', ['x', 'y'])
Line  = collections.namedtuple('Line' , ['p', 'q'])


def diagonal (line):
    """Indicates whether or not `line` is diagonal."""
    return (line.p.x != line.q.x) and (line.p.y != line.q.y)


def lines (filename):
    """ Python iterator over lines in `filename`, return `Line`s."""
    point = lambda s: Point._make( int(t)   for t in s.split(',')  )
    line  = lambda s: Line._make ( point(t) for t in s.split('->') )

    with open(filename) as stream:
        for s in stream.readlines():
            yield line(s)


def points (line):
    """Returns an iterator over `Point`s in `line`.

    The Line `line` must be horizontal, vertical, or diagonal with a
    slope of 45 degrees.
    """
    dx    = line.q.x - line.p.x
    dy    = line.q.y - line.p.y
    sx    = sign(dx)
    sy    = sign(dy)
    steps = max( abs(dx), abs(dy) ) + 1
    x     = line.p.x
    y     = line.p.y

    for s in range(steps):
        yield Point(x, y)
        x += sx
        y += sy


def record (line, vents):
    """Records vent `line`s to `vents` coordinate-to-counts dictionary."""
    for point in points(line):
        vents[point] += 1


def sign (x):
    """Return `-1` if `x < 0`, `0` if `x == 0` and `1` if `x > 0`."""
    return 0 if x == 0 else (1 if x > 0 else -1)


filename  = 'aoc-2021-d05.txt'
vents     = collections.defaultdict(int)
diagonals = collections.defaultdict(int)


# Part 1
#
# Q: At how many points do at least two lines overlap?
# A: Overlap = 6113

for line in lines(filename):
    record(line, diagonals if diagonal(line) else vents)

overlap = sum(1 for count in vents.values() if count >= 2)

print(f'Part 1: Overlap = {overlap:5}')


# Part 2
#
# Q: At how many points do at least two lines overlap (with diagonals)?
# A: Overlap = 20373

vents   = { p: vents[p] + diagonals[p] for p in list(vents) + list(diagonals) }
overlap = sum(1 for count in vents.values() if count >= 2)

print(f'Part 2: Overlap = {overlap:5}')
