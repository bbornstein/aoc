#!/usr/bin/env python3

# Advent of Code 2023, Day 4 (https://adventofcode.com/2023/day/4)
# Author: Ben Bornstein


def card (line):
    """Parse card description on `line` and returns number of matches."""
    winning, have = line.split(':')[1].split('|')
    winning       = set(int(n) for n in winning.split())
    have          = set(int(n) for n in have.split())
    return len(winning & have)


def count (c, matches):
    """Recursively counts copies for card `c` based on `matches`."""
    return matches[c] + sum(count(c + n + 1, matches) for n in range(matches[c]))


def lines (filename, func=None):
    """Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


filename = 'aoc-2023-d04.txt'
matches  = list( lines(filename, card) )


# Part 1
#
# Q: How many points are they worth in total?
# A: Part 1: Total points: 20107

total = sum(2**(m - 1) if m > 0 else 0 for m in matches)
print(f'Part 1: Total points: {total:>7}.')


# Part 2
#
# Q: How many total scratchcards do you end up with?
# A: Part 2: Total cards: 8172507

copies = sum(count(card, matches) for card in range( len(matches) ))
total  = copies + len(matches)
print(f'Part 2: Total cards:  {total:>7}.')
