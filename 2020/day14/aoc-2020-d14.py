#!/usr/bin/env python3

# Advent of Code 2020, Day 14 (https://adventofcode.com/2020/day/14)
# Author: Ben Bornstein


import itertools
import re


def bitwise_or (value, mask):
    """Peforms a bitwise-or operation on `value` and `mask` leaving any
    "bits" marked "X" unchanged.  Note that `value` and `mask` are both
    strings containing '0', '1', or 'X' and a string result is
    returned.
    """
    return ''.join(v if m == '0' else m for v, m in zip(value, mask))


def floating (value):
    """Enumerates and yields all possible binary values for the bit-string
    `value` with "floating" values indicated by "X".  Note that `value`
    is a string containing '0', '1', or 'X' and a string result is
    returned.  For example:

        >>> list( floating('0X') )
        ['00', '01']
    """
    for bits in itertools.product('01', repeat=value.count('X')):
        result = value

        for b in bits:
            result = result.replace('X', b, 1)

        yield result


def load (filename):
    """Loads the Seat Port Computer initialization program from filename,
    yielding a series of tuples per memory write instruction:
    `(mask, addr, value)`.
    """
    pattern = re.compile('mem\[(\d+)\] = (\d+)')

    with open(filename) as stream:
        for line in stream.readlines():
            line = line.strip()

            if line.startswith('mask ='):
                mask = line[7:]
            else:
                match = pattern.search(line)
                addr  = int( match[1] )
                value = int( match[2] )

                yield mask, addr, value


# Part 1
#
# Execute the initialization program.
#
# Q: What is the sum of all values left in memory after it completes?
# (Do not truncate the sum to 36 bits.)
#
# A: Part 1: Sum(memory): 14839536808842.

filename = 'aoc-2020-d14.txt'
memory   = { }
program  = list( load(filename) )

for mask, addr, value in program:
    clear        = int( mask.replace('X', '1'), 2 )
    keep         = int( mask.replace('X', '0'), 2 )
    memory[addr] = (value | keep) & clear

print(f'Part 1: Sum(memory): {sum(memory.values())}.')


# Part 2
#
# Execute the initialization program using an emulator for a version 2
# decoder chip.
#
# Q: What is the sum of all values left in memory after it completes?
# A: Part 2: Sum(memory): 4215284199669.

memory.clear()

for mask, addr, value in program:
    for a in floating( bitwise_or(f'{addr:036b}', mask) ):
        memory[a] = value

print(f'Part 2: Sum(memory): {sum(memory.values())}.')
