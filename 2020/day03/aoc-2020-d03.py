#!/usr/bin/env python3

# Advent of Code 2020, Day 3 (https://adventofcode.com/2020/day/3)
# Author: Ben Bornstein


import collections
import functools


Point   = collections.namedtuple( 'Point', [ 'x' , 'y'] )
Slope   = collections.namedtuple( 'Slope', ['dx', 'dy'] )
product = lambda items: functools.reduce(lambda a, b: a * b, items, 1)


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def move (pos, slope):
    """Returns a new position by moving from `pos` by `slope` amount."""
    return Point(pos.x + slope.dx, pos.y + slope.dy)


def tree (hill, pos):
    """Indicates whether or not hill has a tree at (x, y) `pos`ition."""
    cols = len(hill[0])
    return hill[pos.y][pos.x % cols] == '#'


def trees (hill, slope, start=None):
    """Returns the number of trees encountered down `hill` according to the
    given `slope` trajectory.  If not specified, `start` defaults to
    `Point(0, 0)`.
    """
    pos   = Point(0, 0) if start is None else start
    count = 0

    while pos.y < len(hill):
        count += 1 if tree(hill, pos) else 0
        pos    = move(pos, slope)

    return count


# Part 1
#
# Q: Starting at the top-left corner of your map and following a slope
# of right 3 and down 1, how many trees would you encounter?
# A: Part 1: Trees encountered: 220.

filename = 'aoc-2020-d03.txt'
hill     = list( lines(filename, lambda s: s.strip()) )

ntrees = trees(hill, Slope(3, 1))
print(f'Part 1: Trees encountered: {ntrees}.')


# Part 2
#
# Q: What do you get if you multiply together the number of trees
# encountered on each of the listed slopes?
# A: Part 2: Product of trees encountered: 2138320800.

slopes = Slope(1, 1), Slope(3, 1), Slope(5, 1), Slope(7, 1), Slope(1, 2)
ntrees = [ trees(hill, s) for s in slopes ]
print(f'Part 2: Product of trees encountered: {product(ntrees)}.')
