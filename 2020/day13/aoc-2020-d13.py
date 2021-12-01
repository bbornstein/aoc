#!/usr/bin/env python3

# Advent of Code 2020, Day 13 (https://adventofcode.com/2020/day/13)
# Author: Ben Bornstein


def crt (nrs):
    """Solves a system of modular congruences by finding `x` (return value),
    given a list of modulus factors (n_i's) and remainders (r_i's), such
    that `x` is the smallest positive integer that satisfies the
    following:

        x mod n_1 = r_1
        ...
        x mod n_k = r_k

    Where `nrs = [(n_1, r_1), ... (n_k, r_k)]`.

    The solution uses the Chinese Remainder Theorem [1] and implements a
    Sieve Search [2].  This method is *exponential* time complexity, but
    is *much* more efficient than a systematic (linear) search.  It
    takes only a few hundredths of a second on the puzzle input and is
    incredibly straightforward to implement (and understand).

    [1]: https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    [2]: https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
    """
    ns, rs = zip( *list( reversed( sorted(nrs, key=lambda t: t[0]) ) ) )
    r      = ns[0]
    result = rs[0]

    for i in range(1, len(nrs)):
        while result % ns[i] != rs[i]:
            result += r
        r *= ns[i]

    return result


filename = 'aoc-2020-d13.txt'

with open(filename) as stream:
    depart   = int( stream.readline() )
    schedule = stream.readline().split(',')


# Part 1
#
# Q: What is the ID of the earliest bus you can take to the airport
# multiplied by the number of minutes you'll need to wait for that bus?
#
# A: Part 1: Bus (59) * wait (5) = 295.

buses     = [ int(s) for s in schedule if s != 'x' ]
waits     = [ (b, -depart % b) for b in buses ]
bus, wait = min(waits, key=lambda t: t[1])

print(f'Part 1: Bus ({bus}) * wait ({wait}) = {bus * wait}.')


# Part 2
#
# Q: What is the earliest timestamp such that all of the listed bus IDs
# depart at offsets matching their positions in the list?
#
# A: Part 2: Earliest timestamp: 213890632230818.

buses = [ (pos, int(s)) for pos, s in enumerate(schedule) if s != 'x' ]
nrs   = [ (bus, -pos % bus) for pos, bus in buses ]

print(f'Part 2: Earliest timestamp: {crt(nrs)}.' )
