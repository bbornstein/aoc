#!/usr/bin/env python3

# Advent of Code 2020, Day 15 (https://adventofcode.com/2020/day/15)
# Author: Ben Bornstein


import collections


def play (*start, turns):
    """Plays the North Pole Elves memory game with a list of `start`ing
    number and for the given number of `turns`.  Returns the last number
    spoken (after `turns` rounds).
    """
    last    = start[-1]
    numbers = collections.defaultdict(lambda: collections.deque(maxlen=2))

    for pos, n in enumerate(start):
        numbers[n].append(pos + 1)

    for t in range(len(start) + 1, turns + 1):
        positions = numbers[last]
        last      = 0 if len(positions) == 1 else (t - 1) - positions[0]
        numbers[last].append(t)

    return last


test  = False
turns = 2020

if test:
    assert play(0, 3, 6, turns=turns) ==  436
    assert play(1, 3, 2, turns=turns) ==    1
    assert play(2, 1, 3, turns=turns) ==   10
    assert play(1, 2, 3, turns=turns) ==   27
    assert play(2, 3, 1, turns=turns) ==   78
    assert play(3, 2, 1, turns=turns) ==  438
    assert play(3, 1, 2, turns=turns) == 1836

start  = 0, 13, 16, 17, 1, 10, 6
spoken = play(*start, turns=turns)
print(f'Part 1: The {turns}th number spoken is {spoken}.')

turns = 30000000

if test:
    assert play(0, 3, 6, turns=turns) ==  175594
    assert play(1, 3, 2, turns=turns) ==    2578
    assert play(2, 1, 3, turns=turns) == 3544142
    assert play(1, 2, 3, turns=turns) ==  261214
    assert play(2, 3, 1, turns=turns) == 6895259
    assert play(3, 2, 1, turns=turns) ==      18
    assert play(3, 1, 2, turns=turns) ==     362

spoken = play(*start, turns=turns)
print(f'Part 2: The {turns}th number spoken is {spoken}.')
