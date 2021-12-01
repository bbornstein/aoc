#!/usr/bin/env python3

# Advent of Code 2020, Day 2 (https://adventofcode.com/2020/day/2)
# Author: Ben Bornstein


import re


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def parse (line):
    """Parses a password line of the form:

           1-3 a: abcde

    and returns its constituent parts, e.g.: (1, 3, 'a', 'abcde').
    """
    m = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line)
    return int( m[1] ), int( m[2] ), m[3], m[4]


# Part 1
# Q: How many passwords are valid according to their policies?
# A: Policy 1 valid passwords: 439.

# Part 2
# Q: How many passwords are valid according to their policies?
# A: Policy 2 valid passwords: 584.

filename = 'aoc-2020-d02.txt'
policy1  = 0
policy2  = 0

for m, n, c, p in lines(filename, parse):
    if p.count(c) in range(m, n + 1):
        policy1 += 1
    if (p[m - 1] == c or p[n - 1] == c) and p[m - 1] != p[n - 1]:
        policy2 += 1

print(f'Policy 1 valid passwords: {policy1}.')
print(f'Policy 2 valid passwords: {policy2}.')
