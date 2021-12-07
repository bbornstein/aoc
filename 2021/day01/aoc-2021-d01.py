#!/usr/bin/env python3

# Advent of Code 2021, Day 1 (https://adventofcode.com/2021/day/1)
# Author: Ben Bornstein


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def windows (seq, size):
    """Yields windows over `seq`uence of `size` items, e.g.:

           windows('ABCD', 2) -> ('A', 'B'), ('B', 'C'), ('C', 'D')
    """
    for n in range(size - 1, len(seq)):
        yield tuple( seq[n - s] for s in range(size - 1, -1, -1) )



filename = 'aoc-2021-d01.txt'
depths   = list( lines(filename, int) )


# Part 1
#
# Q: How many measurements are larger than the previous measurement?
# A: 1715 measurements are larger than the previous measurement.

count = sum( w[1] > w[0] for w in windows(depths, size=2) )
print(f'Part 1: {count} measurements are larger than the previous measurement.')


# Part 2
#
# Q: How many sums are larger than the previous sum?
# A:

sums  = [ sum(w) for w in windows(depths, size=3) ]
count = sum( w[1] > w[0] for w in windows(sums, size=2) )
print(f'Part 2: {count} sums are larger than the previous sum.')
