#!/usr/bin/env python3

# Advent of Code 2023, Day 11 (https://adventofcode.com/2023/day/11)
# Author: Ben Bornstein


import collections
import itertools


Point = collections.namedtuple('Point', ['x', 'y'])

def catalog (image, rows, cols, expansion):
    """Catalogs galaxies in `image` where `rows` and `cols` are lists
    of empty rows and columns which will be "expanded" by `expansion`
    factor.  Returns a `set` of cataloged galaxies, where each galaxy
    is represented by its location (a `Point(x=col, y=row)`).
    """
    galaxies = set()

    r = 0
    for row, data in enumerate(image):
        r += expansion if row in rows else 1
        c  = 0
        for col, datum in enumerate(data):
            c += expansion if col in cols else 1
            if datum == '#':
                galaxies.add( Point(y=r, x=c) )

    return galaxies


def empty (image):
    """Returns a list of empty rows in `image`."""
    return [ r for r, row in enumerate(image) if all(c == '.' for c in row) ]


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def manhattan (p, q):
    """Returns the Manhattan distance between `p` and `q`."""
    return abs(p.x - q.x) + abs(p.y - q.y)


filename = 'aoc-2023-d11.txt'
image    = list( lines(filename, lambda line: [ c for c in line.strip() ] ) )
rows     = empty(image)
cols     = empty( zip(*image) )


# Part 1
#
# Q: What is the sum of these lengths?
# A: Part 1: Sum of lengths (expansion=2): 9795148

galaxies = catalog(image, rows, cols, expansion=2)
pairs    = itertools.combinations(galaxies, 2)
total    = sum(manhattan(p, q) for p, q in pairs if p != q)
print(f'Part 1: Sum of lengths (expansion=2): {total:>14}')


# Part 2
#
# Q: What is the sum of these lengths?
# A: Part 1: Sum of lengths (expansion=1e6): 650672493820

galaxies = catalog(image, rows, cols, expansion=int(1e6))
pairs    = itertools.combinations(galaxies, 2)
total    = sum(manhattan(p, q) for p, q in pairs if p != q)
print(f'Part 2: Sum of lengths (expansion=1e6): {total}')
