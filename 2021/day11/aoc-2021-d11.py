#!/usr/bin/env python3

# Advent of Code 2021, Day 11 (https://adventofcode.com/2021/day/11)
# Author: Ben Bornstein


import functools
import itertools
import operator


def energize (grid, row=None, col=None):
    """Energizes octopus `grid` by increasing energy levels by one.

    If `row` and `col` are given, only the octopus at that grid position
    is energized.  Otherwise all octopuses are energized.
    """
    if row is not None and col is not None:
        grid[row][col] += 1
    else:
        for r, c in iterate(grid):
            energize(grid, row=r, col=c)


def flashed (octopus):
    """Indicates whether `octopus` has flashed."""
    return octopus > 9


def iterate (grid):
    """Returns a `(row, col)` iterable over the 2D `grid`."""
    return itertools.product( *map(range, size(grid) ) )


def load (filename):
    """Loads and returns grid of octopus engery levels from `filename`."""
    with open(filename) as stream:
        for line in stream.readlines():
            yield [ int(c) for c in line.strip() ]


def neighbors (row, col, nrows, ncols):
    """Returns a list of `(r, c)` 8-neighbors (up, down, left, right, and
    diagonals) for `(row, col)`.

    Invalid neighbor coordinates outside the range row and column range
    `[0, nrows)` or `[0, ncols)`, respectively, will not be returned.
    """
    for dr, dc in itertools.product((-1, 0, 1), repeat=2):
        if dr == 0 and dc == 0:
            continue

        r = row + dr
        c = col + dc

        if r in range(nrows) and c in range(ncols):
            yield (r, c)


def propagate (grid):
    """Propagates flashes across `grid` returning the total number of
    flashes seen.
    """
    flashing = [ (r, c) for r, c in iterate(grid) if flashed( grid[r][c] ) ]
    seen     = [ ]

    while len(flashing) > 0:
        row, col = flashing.pop()
        seen.append( (row, col) )

        for r, c in neighbors(row, col, *size(grid)):
            energize(grid, row=r, col=c)

            if flashed( grid[r][c] ):
                if (r, c) not in flashing and (r, c) not in seen:
                    flashing.append( (r, c) )

    return len(seen)


def size (grid):
    """Returns the size of `grid` as `(nrows, ncols)`."""
    return len(grid), len(grid[0])


def settle (grid):
    """Settles `grid` octopuses that have flashed by setting their energy
    level to zero.
    """
    for r, c in iterate(grid):
        if flashed( grid[r][c] ):
            grid[r][c] = 0


filename      = 'aoc-2021-d11.txt'
grid          = list( load(filename) )
num_octopuses = functools.reduce(operator.mul, size(grid), 1)
part          = 0
step          = 0
total         = 0


while True:
    step += 1

    _, num_flashed, _ = energize(grid), propagate(grid), settle(grid)
    total += num_flashed

    # Part 1
    #
    # Q: How many total flashes are there after 100 steps?
    # A: Total Flashes = 1732

    if step == 100:
        print(f'Part 1: Total Flashes  = {total}')
        part += 1

    # Part 2
    #
    # Q: What is the first step during which all octopuses flash?
    # A: All Flash Step = 290

    if num_flashed == num_octopuses:
        print(f'Part 2: All Flash Step = {step:4}')
        part += 1

    if part == 2:
        break
