#!/usr/bin/env python3

# Advent of Code 2023, Day 6 (https://adventofcode.com/2023/day/6)
# Author: Ben Bornstein

import math


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def number (line):
    """Returns a single number on a `line`.  For example, a `line` of:

        Time:      7  15   30

    Returns `71530`.
    """
    return int( line.split(':')[1].replace(' ', '') )


def numbers (line):
    """Returns a list of numbers on a `line`.  For example, a `line` of:

        Distance:  9  40  200

    Returns `[9, 40, 200]`.
    """
    return [ int(s) for s in line.split(':')[1].split() ]


def ways (time, distance):
    """Return the number of ways to beat `distance` for race `time`."""
    return sum(1 for hold in range(time) if (hold * (time - hold)) > distance)


filename = 'aoc-2023-d06.txt'


# Part 1
#
# Q: What do you get if you multiply these numbers together?
# A: Part 1: Product of wins: 1731600.

times, distances = lines(filename, numbers)
answer           = math.prod( ways(t, d) for t, d in zip(times, distances) )
print(f'Part 1: Product of wins: {answer:>8}.')


# Part 2
#
# Q: How many ways can you beat the record in this one much longer race?
# A: Part 2: Number of wins: 40087680.

time, distance = lines(filename, number)
print(f'Part 2: Number  of wins: {ways(time, distance):>8}.')
