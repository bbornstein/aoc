#!/usr/bin/env python3

# Advent of Code 2023, Day 3 (https://adventofcode.com/2023/day/3)
# Author: Ben Bornstein


import collections
import math
import re


def adjacent (match, row, schematic):
    """Indicates whether part number `match` (on `row` in `schematic`)
    is adjacent to a symbol.
    """
    return any(symbol(schematic[r][c]) for r, c in neighborhood(match, row))


def catalog_gears (match, row, schematic, catalog):
    """Builds a catalog of gears by appending part number `match` (on
    `row` in `schematic`) to the list `catalog[(r, c])` if `match` is
    adjacent to a gear.

    The coordinates `r` and `c` are the row and column location of the
    gear within the `schematic`.
    """
    for r, c in neighborhood(match, row):
        if schematic[r][c] == '*':
            catalog[(r, c)].append( int(match[0]) )
            break


def load (filename):
    """Loads engine schematic from `filename`."""
    with open(filename) as stream:
        schematic = [ f'\n{line}' for line in stream.readlines() ]

    pad = '\n' * len(schematic[0])
    schematic.insert(0, pad)
    schematic.append(pad)

    return schematic


def neighborhood (match, row):
    """Yields the neighborhood "around" a part number `match` on `row`."""
    for delta in (-1, 0, 1):
        for col in range(match.start(0) - 1, match.end(0) + 1):
            yield (row + delta, col)


def symbol (c):
    """Indicates whether `c` is a schematic symbol."""
    return not c.isdigit() and c != '.' and c != '\n'


filename  = 'aoc-2023-d03.txt'
schematic = load(filename)
matches   = [ ]

for row, line in enumerate(schematic):
    matches += [ (row, m) for m in re.finditer('\d+', line) if m is not None ]


# Part 1
#
# Q: What is the sum of all of the part numbers in the engine schematic?
# A: Part 1: The sum of all part numbers is 527446.

total = sum(int(m[0]) for row, m in matches if adjacent(m, row, schematic))
print(f'Part 1: The sum of all part numbers is {total:>8}.')


# Part 2
#
# Q: What is the sum of all of the gear ratios in your engine schematic?
# A: Part 2: The sum of all gear ratios is 73201705.

catalog = collections.defaultdict(list)

for row, match in matches:
    catalog_gears(match, row, schematic, catalog)

ratios = sum( math.prod(gears) for gears in catalog.values() if len(gears) > 1 )
print(f'Part 2: The sum of all gear ratios  is {ratios:>8}.')
