#!/usr/bin/env python3

# Advent of Code 2021, Day 8 (https://adventofcode.com/2021/day/8)
# Author: Ben Bornstein


import itertools


def decode (outputs, ring):
    """Decodes LED segment `outputs` according to the decoder `ring` which
    maps LED segment patterns to digits [0, 9].
    """
    digits = [ ring[normalize(pattern)] for pattern in reversed(outputs) ]
    return sum( digit * (10**place) for place, digit in enumerate(digits) )


def deduce (patterns):
    """Deduces LED segments from `patterns` to decode the digits [0, 9].
    Returns a "decoder ring" which maps a single LED pattern to its
    corresponding digit.

    See also `decode()`.
    """
    # Lookup the four unique LED digits based on their pattern length.
    digits = { 2: 1, 4: 4, 3: 7, 7: 8 }
    ring   = { digits[len(p)]: set(p) for p in patterns if len(p) in digits }

    for p in map(set, patterns):

        # Three digits have five LED segments: 2, 3, 5
        # Comparison (conditional) order is significant!
        if len(p) == 5:
            if len(p - ring[1]) == 3:
                ring[3] = p
            elif len(p - ring[4]) == 2:
                ring[5] = p
            else:
                ring[2] = p

        # Three digits have six LED segments: 0, 6, 9
        # Comparison (conditional) order is significant!
        elif len(p) == 6:
            if len(p - ring[4]) == 2:
                ring[9] = p
            elif len(p - ring[1]) == 4:
                ring[0] = p
            else:
                ring[6] = p

    return { normalize(pattern): digit for digit, pattern in ring.items() }


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def normalize (pattern):
    """Normalizes the LED segment `pattern` by sorting it alphabetically."""
    return ''.join( sorted(pattern) )


filename = 'aoc-2021-d08.txt'
entries  = list( lines(filename, lambda line: line.replace('|', '').split()) )


# Part 1
#
# Q: In the output values, how many times do digits 1, 4, 7, or 8 appear?
# A: Count = 26

outputs = itertools.chain(*[ entry[10:] for entry in entries ])
count   = sum(1 for output in outputs if len(output) in (2, 3, 4, 7))
print(f'Part 1: Count = {count:7}')


# Part 2
#
# Q: What do you get if you add up all of the output values?
# A: Total = 1009098

total = sum( decode(entry[10:], deduce(entry[:10])) for entry in entries )
print(f'Part 2: Total = {total}')
