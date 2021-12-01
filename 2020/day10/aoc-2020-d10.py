#!/usr/bin/env python3

# Advent of Code 2020, Day 10 (https://adventofcode.com/2020/day/10)
# Author: Ben Bornstein


import collections
import functools
import itertools


product = lambda items: functools.reduce(lambda a, b: a * b, items, 1)


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


# Part 1
#
# Q: What is the number of 1-jolt differences multiplied by the number
# of 3-jolt differences?
#
# A: Part 1: Number of 1-jolt * 3-jolt differences: 1885.

filename = 'aoc-2020-d10.txt'
adapters = sorted( lines(filename, int) )
adapters.insert(0, 0)
adapters.append( adapters[-1] + 3 )

deltas = [ adapters[n] - adapters[n - 1] for n in range(1, len(adapters)) ]
counts = collections.Counter(deltas)
result = counts[1] * counts[3]
print(f'Part 1: Number of 1-jolt * 3-jolt differences: {result}.')


# Part 2
#
# Q: What is the total number of distinct ways you can arrange the
# adapters to connect the charging outlet to your device?
#
# A: Part 2: Combinations: 2024782584832.

factor  = { 1: 1, 2: 2, 3: 4, 4: 7 }
runs    = [ len( list(g) ) for k, g in itertools.groupby(deltas) if k == 1 ]
combos  = product([ factor[r] for r in runs ])

print(f'Part 2: Total combinations: {combos}.')


# Runs of ones (1) in the "jolts" deltas yield different multiplication
# factors when computing the total number of combinations (product of
# factors).  I counted factors by hand for for 1, 2, and 3 based on the
# examples provided in the puzzle description:
#
# Deltas: 1   3   1   1   1   3    1    1    3    1    3    3
#     (0)   1   4   5   6   7   10   11   12   15   16   19   (22)
#     (0)   1   4   5   6   7   10        12   15   16   19   (22)
#     (0)   1   4   5       7   10   11   12   15   16   19   (22)
#     (0)   1   4   5       7   10        12   15   16   19   (22)
#     (0)   1   4       6   7   10   11   12   15   16   19   (22)
#     (0)   1   4       6   7   10        12   15   16   19   (22)
#     (0)   1   4           7   10   11   12   15   16   19   (22)
#     (0)   1   4           7   10        12   15   16   19   (22)
#
# Notice that:
#
#   1.  A single "run" of 1 can never be deleted when deriving
#       combinations, so it's factor is 1 (combos *= 1).
#
#   2.  A run of two 1s can result in a single deletion, so the total
#       number of combinations is two (on/present or off/absent)
#      (combos *= 2).
#
#   3.  A run of three 1s results in four possible combinations.  While
#       2^3 = 8, certain deletions would result in a delta of more than
#       three "jolts", given that runs are (by definition) bracketed by
#       deltas of three:
#
#           000 <-- Invalid
#           001
#           010 <-- Invalid
#           011
#           100 <-- Invalid
#           101
#           110 <-- Invalid
#           111
#
#   4.  A run of four 1s can result in seven possible combinations
#       (combos *= 7).  It's derivation is left as an exercise for
#       the reader. :)
#
#  I must admit, I stopped at runs of four 1s when I saw that was the
#  longest run given my puzzle input.  This is arguably "cheating" and
#  not the most general solution.
