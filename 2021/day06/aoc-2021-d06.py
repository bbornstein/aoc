#!/usr/bin/env python3

# Advent of Code 2021, Day 6 (https://adventofcode.com/2021/day/6)
# Author: Ben Bornstein


import collections


def load (filename):
    """Loads the initial latern fish state from `filename`."""
    with open(filename) as stream:
        return [ int(s) for s in stream.read().split(',') ]


def fishogram (fish):
    """Creates a histogram of `fish`, providing a count of fish for each
    number of days remaining before their next spawn cycle, i.e.:

        F[days_remaining] = count
    """
    return collections.Counter(fish)


def spawn (fish, days):
    """Spawns `fish` for `days` and returns the total number of fish."""
    today = fishogram(fish)

    for day in range(days):
        tomorrow = collections.defaultdict(int)
        for remaining, count in today.items():
            if remaining == 0:
                tomorrow[6] += count
                tomorrow[8] += count
            else:
                tomorrow[remaining - 1] += count
        today = tomorrow

    return sum( today.values() )


filename = 'aoc-2021-d06.txt'
fish     = load(filename)


# Part 1
#
# Q: How many lanternfish would there be after 80 days?
# A: Fish = 386640

print(f'Part 1: Fish = {spawn(fish,  80):13}')


# Part 2
#
# Q: How many lanternfish would there be after 256 days?
# A: Fish = 1733403626279

print(f'Part 2: Fish = {spawn(fish, 256):13}')
