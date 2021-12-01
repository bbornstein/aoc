#!/usr/bin/env python3

# Advent of Code 2020, Day 6 (https://adventofcode.com/2020/day/6)
# Author: Ben Bornstein

import collections


# Part 1
#
# Q: For each group, count the number of questions to which anyone
# answered "yes".  What is the sum of those counts?
# A: Part 1: Sum of counts: 6351.

# Part 2
#
# Q: For each group, count the number of questions to which everyone
# answered "yes".  What is the sum of those counts?
# A: Part 2: Sum of counts: 3143.

filename  = 'aoc-2020-d06.txt'
people    = 0
questions = collections.Counter()
anyone    = 0
everyone  = 0

with open(filename) as stream:
    for line in stream.readlines():
        line = line.strip()
        if len(line) == 0:
            anyone   += len(questions)
            everyone += len([ v for v in questions.values() if v == people ])
            people    = 0
            questions.clear()
        else:
            people += 1
            questions.update(line)

anyone   += len(questions)
everyone += len([ v for v in questions.values() if v == people ])

print(f'Part 1: Sum of counts: {anyone}.')
print(f'Part 2: Sum of counts: {everyone}.')
