#!/usr/bin/env python3

# Advent of Code 2023, Day 6 (https://adventofcode.com/2023/day/6)
# Author: Ben Bornstein

import math


def ways (time, distance):
    """Return the number of ways to beat `distance` for race `time`."""
    return sum(1 for hold in range(time) if (hold * (time - hold)) > distance)


filename = 'aoc-2023-d06.txt'

with open(filename) as stream:
    times     = [ int(s) for s in stream.readline().split(':')[1].split() ]
    distances = [ int(s) for s in stream.readline().split(':')[1].split() ]


# Part 1
#
# Q: What do you get if you multiply these numbers together?
# A: Part 1: Multiply race ways: 1731600.

answer = math.prod( ways(t, d) for t, d in zip(times, distances) )
print(f'Part 1: Product of wins: {answer:>8}.')


with open(filename) as stream:
    time     = int( stream.readline().split(':')[1].replace(' ', '') )
    distance = int( stream.readline().split(':')[1].replace(' ', '') )


# Part 2
#
# Q: How many ways can you beat the record in this one much longer race?
# A: Part 2: Record beating ways: 40087680.

print(f'Part 2: Number  of wins: {ways(time, distance):>8}.')
