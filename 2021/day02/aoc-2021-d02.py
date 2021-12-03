#!/usr/bin/env python3

# Advent of Code 2021, Day 2 (https://adventofcode.com/2021/day/2)
# Author: Ben Bornstein


def command (line):
    """Converts `line` into a `(direction, magnitude)` submarine command."""
    direction, magnitude = line.split()
    return direction, int(magnitude)


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line



filename = 'aoc-2021-d02.txt'
commands = list( lines(filename, command) )


# Part 1
#
# Q: Multiply your final horizontal position by your final depth?
# A: Part 1: 1925 pos * 879 depth = 1692075

depth = 0
pos   = 0

for direction, magnitude in commands:
    if direction == 'forward':
        pos += magnitude
    else:
        if direction == 'up':
            magnitude *= -1

        depth += magnitude

print(f'Part 1: {pos} pos * {depth:6} depth = {pos * depth:10}')


# Part 2
#
# Q: Multiply your final horizontal position by your final depth?
# A: Part 2: 1925 pos * 908844 depth = 1749524700

aim   = 0
depth = 0
pos   = 0

for direction, magnitude in commands:
    if direction == 'forward':
        pos   += magnitude
        depth += aim * magnitude
    else:
        if direction == 'up':
            magnitude *= -1

        aim += magnitude

print(f'Part 2: {pos} pos * {depth:6} depth = {pos * depth:10}')
