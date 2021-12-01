#!/usr/bin/env python3

# Advent of Code 2020, Day 1 (https://adventofcode.com/2020/day/1)
# Author: Ben Bornstein


import functools
import itertools


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


# Part 1
#
# Q: What is the product of the two entries that sum to 2020?
# A: Sum of (527, 1493) is 2020 and product is 786811.

# Part 2
#
# Q: What is the product of the three entries that sum to 2020?
# A: Sum of (1111, 289, 620) is 2020 and product is 199068980.


filename = 'aoc-2020-d01.txt'
entries  = list( lines(filename, int) )
product  = lambda items: functools.reduce(lambda a, b: a * b, items, 1)

for r in 2, 3:
    for values in itertools.combinations(entries, r):
        if sum(values) == 2020:
            print(f'Sum of {values} is 2020 and product is {product(values)}.')
            break
