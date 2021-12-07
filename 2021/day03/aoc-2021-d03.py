#!/usr/bin/env python3

# Advent of Code 2021, Day 3 (https://adventofcode.com/2021/day/3)
# Author: Ben Bornstein


import functools


def colsum (matrix, column=None):
    """Returns the column-wise sum of `matrix` (a vector) or, if a specific
    `column` index is provided, the sum of only that column (a scalar).
    """
    if column is None:
        return functools.reduce(dotadd, matrix)
    else:
        return sum(matrix[row][column] for row in range(len(matrix)))


def dotadd (vec1, vec2):
    """Adds `vec1` and `vec2` element-wise."""
    return [ e1 + e2 for e1, e2 in zip(vec1, vec2) ]


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def rating (numbers, criteria):
    """Finds and returns the submarine oxygen (O2) generator rating or
    carbon dioxide (CO2) scrubber rating contained in `numbers`.  The
    `numbers` matrix is iteratively searched until a single number (row)
    remains by:

      1. First finding the most common bit in a bit position, and
      2. Keeping only those numbers where:

           numbers[row][pos] == criteria(most_common)

      3. Repeating with the next bit position

     Where:

       * `row` is the row (representing a value) in the `numbers` matrix
       * `pos` is the bit position within a `number[row]`
       * `most_common` is:
            * `>  0`  if `1` is the most common bit in `numbers[:][pos]`
            * `<  0`  if `0` is the most common bit in `numbers[:][pos]`
            * `== 0`  if `0` and `1` are equally common

    The function `criteria(most_common)` should return `1` to keep
    numbers where `numbers[:][pos] == 1` and `-1` to keep numbers where
    `numbers[:][pos] == 0`.
    """
    indices = list( range( len(numbers) ) )
    nbits   = len(numbers[0])
    value   = None

    for pos in range(nbits):
        most_common = colsum( subset(numbers, indices), column=pos )

        if len(indices) == 1:
            value = vec2int( numbers[ indices[0] ] )
            break
        else:
            keeper  = criteria(most_common)
            indices = [ n for n in indices if numbers[n][pos] == keeper ]

    return value


def str2vec (s):
    """Converts the binary string of '0' and '1' characters to a vector.

    An element of the resulting vector is `-1` if the binary string
    contains a `'0'` at the corresponding bit position, otherwise the
    element is `1`.
    """
    return [ -1 if c == '0' else 1 for c in s.strip() ]


def subset (matrix, indices):
    """Returns a subset of `matrix` rows that correspond to `indices`."""
    return [ matrix[index] for index in indices ]


def vec2int (vec):
    """Converts `vec`tor to an integer.

    Each element in `vec` represents a bit in the integer.  The bit is
    `1` if the element is greater than zero, otherwise the bit is `0`.
    """
    return functools.reduce(lambda n, elem: (n << 1) | (elem > 0), vec, 0)



filename = 'aoc-2021-d03.txt'
numbers  = list( lines(filename, str2vec) )


# Part 1
#
# Q: What is the power consumption of the submarine?
# A: 1869 gamma * 2226 epsilon = 4160394

nbits   = len(numbers[0])
gamma   = vec2int( colsum(numbers) )
epsilon = ~gamma & (2**nbits - 1)

print(f'Part 1: {gamma} gamma * {epsilon} epsilon = {gamma * epsilon}')


# Part 2
#
# Q: Multiply your final horizontal position by your final depth?
# A: 1719 O2 * 2400 CO2 = 4125600


O2  = rating(numbers, lambda most_common:  1 if most_common >= 0 else -1)
CO2 = rating(numbers, lambda most_common: -1 if most_common >= 0 else  1)

print(f'Part 2: {O2} O2    * {CO2} CO2     = {O2 * CO2}')
