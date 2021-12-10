#!/usr/bin/env python3

# Advent of Code 2021, Day 10 (https://adventofcode.com/2021/day/10)
# Author: Ben Bornstein


import collections
import functools


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


filename   = 'aoc-2021-d10.txt'
closes     = { '(': ')', '[': ']', '{': '}' , '<': '>'   }
closers    = closes.values()
counts     = collections.defaultdict(int)
incomplete = [ ]


for line in lines(filename):
    error = False
    line  = line.strip()
    stack = [ ]

    for c in line:
        stack.append(c)

        if c not in closers or len(stack) < 2:
            continue

        actual   = stack[-1]
        expected = closes[ stack[-2] ]

        if actual == expected:
            stack.pop()
            stack.pop()
        else:
            counts[actual] += 1
            error = True
            break

    if not error:
        incomplete.append(stack)


# Part 1
#
# Q: What is the total syntax error score for those errors?
# A: Score = 319329

points = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
score  = sum( count * points[c] for c, count in counts.items() )
print(f'Part 1: Score = {score:10}')


# Part 2
#
# Q: What is the middle score?
# A: 3515583998

points = { ')': 1, ']': 2, '}': 3, '>': 4 }
scores = [ ]

for stack in incomplete:
    complete = [ closes[c] for c in reversed(stack) ]
    score    = functools.reduce(lambda a, c: (a * 5) + points[c], complete, 0)
    scores.append(score)

scores.sort()
print(f'Part 2: Score = {scores[len(scores) // 2]}')
