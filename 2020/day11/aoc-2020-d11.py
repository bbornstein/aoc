#!/usr/bin/env python3

# Advent of Code 2020, Day 11 (https://adventofcode.com/2020/day/11)
# Author: Ben Bornstein

import copy
import itertools


EMPTY      = 0
OCCUPIED   = 1
FLOOR      = 2
CharToInt  = { 'L': EMPTY, '#': OCCUPIED, '.': FLOOR }
Directions = ( (-1, -1), (0, -1), (1, -1),
               (-1,  0),          (1,  0),
               (-1,  1), (0,  1), (1,  1) )


def adjacent (area, r, c, radius=None):
    """Returns the adjacent seats within `radius` of the seat at row (`r`)
    and column (`c`) in all directions (up, down, left, right, and
    diagonals).  If `radius` is one (1), adjacent seats are the
    surrounding 3x3 neighborhood.  If `radius` is `None` (default),
    adjacent seats are the sight-lines in each direction (until the
    first seat in that direction is encountered) around the seat at row
    (`r`) and column (`c`).
    """
    nrows = len( area    )
    ncols = len( area[0] )

    for dr, dc in Directions:
        nr   = r
        nc   = c
        r0   = 0
        spot = FLOOR

        while spot == FLOOR and (radius is None or r0 < radius):
            r0 += 1
            nr += dr
            nc += dc

            if nr not in range(nrows) or nc not in range(ncols):
                break
            else:
                spot = area[nr][nc]

        if spot != FLOOR:
            yield spot


def apply (area, next, neighborhood, threshold):
    """Applies puzzle rules to the seating `area`, storing updates in the
    `next` seating area.  The parameter `neighborhood` is a function
    that takes a seating `area` and specific seat location (row, column)
    as input (`neighborhood(area, row, col)`) and returns nearby seats
    in that neighborhood.  The parameter `threshold` is the minimum
    number of `OCCUPIED` neighborhood seats required to make a seat
    `EMPTY`.
    """
    for seat, r, c in seats(area):
        neighbors = neighborhood(area, r, c)
        if seat == EMPTY:
            if all(n == EMPTY for n in neighbors):
                next[r][c] = OCCUPIED
        else:
            if len([ n for n in neighbors if n == OCCUPIED ]) >= threshold:
                next[r][c] = EMPTY


def count (area, state=OCCUPIED):
    """Returns the count of spots in the seating `area` in the given state,
    defaulting to `OCCUPIED`.
    """
    return sum(int(pos == state) for row in area for pos in row)


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def merge (dst, src):
    """Merges the source (`src`) seating area into the destination (`dst`)
    seating area and returns the number of changed seats.  A return
    value of zero indicates `dst` and `src` are identical.
    """
    changed = 0

    for seat, r, c in seats(dst):
        if dst[r][c] != src[r][c]:
            changed   += 1
            dst[r][c]  = src[r][c]

    return changed


def parse (line):
    """Parse line into an array of numbers (`EMPTY`, `OCCUPIED`, or `FLOOR`)
    for each spot in the seatring area.
    """
    return [ CharToInt[c] for c in line.strip() ]


def seats (area):
    """An iterator (generator) over seats (either `OCCUPIED` or `EMPTY`) in
    the seating `area`.  Yields a tuple indicating the seat state and
    its row and column location, i.e. `(seat, r, c)`.
    """
    nrows = len( area    )
    ncols = len( area[0] )

    for r, c in itertools.product(range(nrows), range(ncols)):
        if area[r][c] != FLOOR:
            yield area[r][c], r, c


# Part 1
#
# Simulate your seating area by applying the seating rules repeatedly
# until no seats change state.
#
# Q: How many seats end up occupied?
# A: Part 1: Iterations: 94, Occupied 2275.


# Part 2
#
# Q: Given the new visibility method and the rule change for occupied
# seats becoming empty, once equilibrium is reached, how many seats end
# up occupied?
# A: Part 2: Iterations: 86, Occupied 2121.

filename = 'aoc-2020-d11.txt'
area     = list( lines(filename, parse) )
adj3x3   = lambda area, r, c: adjacent(area, r, c, radius=1)
part     = 0


for neighborhood, threshold in (adj3x3, 4), (adjacent, 5):
    curr  = copy.deepcopy(area)
    next  = copy.deepcopy(area)
    iters = 0
    part += 1

    while True:
        iters += 1
        apply(curr, next, neighborhood, threshold)

        if merge(curr, next) == 0:
            break

    print(f'Part {part}: Iterations: {iters}, Occupied {count(curr)}.')
