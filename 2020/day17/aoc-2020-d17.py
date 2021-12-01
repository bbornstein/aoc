#!/usr/bin/env python3

# Advent of Code 2020, Day 17 (https://adventofcode.com/2020/day/17)
# Author: Ben Bornstein


import itertools


def cycle (active):
    """Runs a single cycle of Conways Cubes."""
    coords     = list( transpose( active.keys() ) )
    dimensions = len(coords)
    next       = { }
    ranges     = [ ]


    for d in range(dimensions):
        ranges.append( range( min(coords[d]) - 1, max(coords[d]) + 2 ) )

    for coord in itertools.product(*ranges):
        nactive = sum(1 for n in neighbors(coord) if n in active)
        state   = False

        if coord in active:
            state = nactive == 2 or nactive == 3
        else:
            state = nactive == 3

        if state == True:
            next[coord] = True

    return next


def embed (active, dimensions=3):
    """Embeds a two dimensional mapping of active coordinates in, and
    returns, a higher dimensional mapping, e.g.:

        embed( {(x, y): True}, dimenions=3) -> {(x, y, 0): True}

    """
    return { coord + ((0, ) * (dimensions - 2)): True for coord in active }


def load (filename):
    """Loads the two dimensional Conway Cubes puzzle input and returns a
    mapping of all active coordinates, i.e. `active[coord] = True`.
    """
    active = { }

    with open(filename) as stream:
        for y, line in enumerate( stream.readlines() ):
            line = line.strip()
            for x, c in enumerate(line):
                if c == '#':
                    active[(x, y)] = True

    return active


def neighbors (coord):
    """Returns the coordinates of all 1-neighbors of `coord`.
    """
    for deltas in itertools.product( (-1, 0, 1), repeat=len(coord) ):
        if all(d == 0 for d in deltas):
            continue

        yield tuple( map(sum, zip(coord, deltas)) )


def transpose (coords):
    """Returns the transpose of `coords` in any number of dimensions, so:

        ( (x1, y1, ...), ... (xN, yN, ...) )

    becomes:

        ( (x1, x2, ..., xN), (y1, y2, yN...), ... )

    """
    return zip(*coords)


# Parts 1
#
# Starting with your given initial configuration, simulate six cycles.
#
# Q: How many cubes are left in the active state after the sixth cycle?
# A: Part 1: Active cubes: 289.

# Part 2
#
# Starting with your given initial configuration, simulate six cycles in
# a 4-dimensional space.
#
# Q: How many cubes are left in the active state after the sixth cycle?
# A: Part 2: Active cubes: 2084.

filename = 'aoc-2020-d17.txt'
start    = load(filename)

for dimension in (3, 4):
    active = embed(start, dimension)

    for c in range(6):
        active = cycle(active)

    print(f'Part {dimension - 2}: Active cubes: { len( active.values() ) }.')
