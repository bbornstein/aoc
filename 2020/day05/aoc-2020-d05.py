#!/usr/bin/env python3

# Advent of Code 2020, Day 5 (https://adventofcode.com/2020/day/5)
# Author: Ben Bornstein


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def seat (bpass):
    """Returns the seat ID for the given boarding pass (`bpass`)."""
    row = sum(2**(6-n) for n, s in enumerate(bpass[0:7]) if s == 'B')
    col = sum(2**(2-n) for n, s in enumerate(bpass[7:] ) if s == 'R')
    return (row * 8) + col


# Part 1
#
# Q: What is the highest seat ID on a boarding pass?
# A: Part 1: Highest Seat ID: 885.

filename = 'aoc-2020-d05.txt'
seats    = sorted( lines(filename, seat) )

print(f'Part 1: Highest Seat ID: {seats[-1]}.')


# Part 2
#
# Your seat wasn't at the very front or back, though; the seats with IDs
# +1 and -1 from yours will be in your list.
#
# Q: What is the ID of your seat?
# A: Part 2: My Seat ID: 623.

for n in range(1, len(seats)):
    if seats[n - 1] == (seats[n] - 2):
        print(f'Part 2: My Seat ID: {seats[n] - 1}.')
        break
