#!/usr/bin/env python3

# Advent of Code 2023, Day 2 (https://adventofcode.com/2023/day/2)
# Author: Ben Bornstein


import collections


Cubes      = collections.namedtuple('Cubes', 'red green blue', defaults=3 * [0])
Cubes.make = lambda s: Cubes(
    **{ color: int(n) for n, color in [cubes.split() for cubes in s.split(',')] }
)


def game (line):
    """Parses a game description in `line` and returns (game, [ Cubes ...] )."""
    game, rest = line.strip().split(':')
    return int(game[4:]), [ Cubes.make(sets) for sets in rest.split(';') ]


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def possible (cubes, red=12, green=13, blue=14):
    """Indicates whether a game is possible given a set of `cubes`."""
    return cubes.red <= red and cubes.green <= green and cubes.blue <= blue


def power (sets):
    """Returns the power of the minimum set of cubes in game `sets`."""
    return ( max(cubes.red   for cubes in sets) *
             max(cubes.green for cubes in sets) *
             max(cubes.blue  for cubes in sets) )


filename = 'aoc-2023-d02.txt'
games    = list( lines(filename, game) )


# Part 1
#
# Q: What is the sum of the IDs of those games?
# A: Part 1: The sum of all possible game IDs is 2545.

total = sum(g for g, sets in games if all(possible(cubes) for cubes in sets))
print(f'Part 1: The sum of all possible game IDs is {total}.')


# Part 2
#
# Q: What is the sum of the power of these sets?
# A: Part 2: The sum of the power of these sets is 78111.

total = sum(power(sets) for g, sets in games)
print(f'Part 2: The sum of the power of these sets is {total}.')
