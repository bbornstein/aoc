#!/usr/bin/env python3

# Advent of Code 2021, Day 7 (https://adventofcode.com/2021/day/7)
# Author: Ben Bornstein

import collections


def align (crabs, cost):
    """Aligns the crab positions `crabs` (array) to the same position using
    the least fuel, according to the given `cost` function.  The `cost`
    function takes a single parameter, the number of steps to move,
    i.e. `cost(steps)`.

    Returns `(pos, fuel)`.
    """
    fuel = collections.defaultdict(int)

    for moveto in range( max(crabs) ):
        for crab in crabs:
            fuel[moveto] += cost( abs(crab - moveto) )

    return min(fuel.items(), key=lambda pair: pair[1])


def load (filename):
    """Loads crab position from `filename`."""
    with open(filename) as stream:
        return [ int(s) for s in stream.read().split(',') ]


filename = 'aoc-2021-d07.txt'
crabs    = load(filename)


# Part 1
#
# Q: How much fuel must they spend to align to that position?
# A: Moving to position 328 costs 328187 fuel.

pos, fuel = align(crabs, lambda steps: steps)
print(f'Part 1: Moving to position {pos} costs {fuel:8} fuel.')


# Part 2
#
# Q: How much fuel must they spend to align to that position?
# A: Moving to position 464 costs 91257582 fuel.

pos, fuel = align(crabs, lambda steps: int(steps * (steps + 1) / 2) )
print(f'Part 2: Moving to position {pos} costs {fuel:8} fuel.')
