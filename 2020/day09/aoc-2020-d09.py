#!/usr/bin/env python3

# Advent of Code 2020, Day 9 (https://adventofcode.com/2020/day/9)
# Author: Ben Bornstein


import itertools


def find_sum_range (numbers, n):
    """Returns (i, j) such that sum(numbers[i:j]) == n."""
    cumsum = list( itertools.accumulate(numbers) )

    for j in range(1, len(cumsum)):
        for i in range(0, j):
            if cumsum[j] - cumsum[i] == n:
                return i, j


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


# Part 1
#
# The first step of attacking the weakness in the XMAS data is to find
# the first number in the list (after the preamble) which is not the sum
# of two of the 25 numbers before it.
#
# Q: What is the first number that does not have this property?
# A: Part 1: First number not sum of previous 25: 31161678.


filename = 'aoc-2020-d09.txt'
numbers  = list( lines(filename, int) )
preamble = 25
queue    = numbers[:preamble]

for n in numbers[preamble:]:
    delta = [n - q for q in queue]
    if not any([ (d in queue and (n - d) != d) for d in delta ]):
        print(f'Part 1: First number not sum of previous {preamble}: {n}.')
        break

    queue.pop(0)
    queue.append(n)


# Part 2
#
# Find a contiguous set of at least two numbers in your list which sum
# to the invalid number from Step 1.
#
# Q: What is the encryption weakness in your XMAS-encrypted list of numbers?
# A: Part 2: Encryption weakness: 5453868.

i, j   = find_sum_range(numbers, n)
subset = numbers[i:j]
print(f'Part 2: Encryption weakness: {min(subset) + max(subset)}.')
