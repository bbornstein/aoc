#!/usr/bin/env python3

# Advent of Code 2021, Day 9 (https://adventofcode.com/2021/day/9)
# Author: Ben Bornstein


import itertools


def flood (row, col, heights, basin=None):
    """Return the basin surrounding `(row, col)` in `heights` using a
    recursive flood fill.
    """
    basin = [ ] if basin is None else basin
    nrows = len(heights)
    ncols = len(heights[0])

    basin.append( (row, col) )

    for r, c in neighbors(row, col, nrows, ncols):
        if (r, c) not in basin and heights[r][c] != 9:
            flood(r, c, heights, basin)

    return basin


def load (filename):
    """Loads height map from `filename`."""
    with open(filename) as stream:
        for line in stream.readlines():
            yield [ int(c) for c in line.strip() ]


def neighbors (row, col, nrows, ncols):
    """Returns a list of `(r, c)` 4-neighbors (up, down, left, right) for
    `(row, col)`.

    Invalid neighbor coordinates outside the range row and column range
    `[0, nrows]` or `[0, ncols]`, respectively, will not be returned.
    """
    deltas = (-1, 0), (0, -1), (1, 0), (0, 1)
    valid  = lambda r, c: r in range(0, nrows) and c in range(0, ncols)
    return [ (row + r, col + c) for r, c in deltas if valid(row + r, col + c) ]


filename  = 'aoc-2021-d09.txt'
heights   = list( load(filename) )
nrows     = len(heights)
ncols     = len(heights[0])
locations = [ ]


# Part 1
#
# Q: What is the sum of the risk levels of all low points on your heightmap?
# A: Risk = 486

for row, col in itertools.product( range(nrows), range(ncols) ):
    current  = heights[row][col]
    adjacent = neighbors(row, col, nrows, ncols)

    if all(current < heights[r][c] for r, c in adjacent):
        locations.append((row, col))

risk = sum(heights[row][col] + 1 for row, col in locations)
print(f'Part 1: Risk    = {risk:7}')


# Part 2
#
# Q: Multiply together the sizes of the three largest basins?
# A: Largest = 1059300

sizes   = sorted([ len(flood(row, col, heights)) for row, col in locations ])
largest = sizes[-1] * sizes[-2] * sizes[-3]
print(f'Part 2: Largest = {largest}')
