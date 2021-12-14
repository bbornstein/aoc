#!/usr/bin/env python3

# Advent of Code 2021, Day 14 (https://adventofcode.com/2021/day/14)
# Author: Ben Bornstein


import collections
import itertools


def counterize (counter, rulemers):
    """Applies reaction `rulemers` to the current dimer counts in `counter`
    and returns a new set of dimer counts.  This method is analogous to
    `polymerize()`, but operates only on dimer counts.  It does not
    generate the complete polymer.

    See also `dimerize()` and `polymerize()`.
    """
    result = collections.Counter()

    # Every time a dimer rule matches and is applied, two new dimers are
    # produced and the number of new dimers produced equal to the count
    # of the `dimer` that matched.

    # For the example input and puzzle input, there is never a dimer
    # that doesn't match some rule, so the `else`-clause is never
    # executed (and hasn't been tested).

    for dimer in counter:
        if dimer in rulemers:
            result[ rulemers[dimer][0] ] += counter[dimer]
            result[ rulemers[dimer][1] ] += counter[dimer]
        else:
            result[dimer] = counter[dimer]

    return result


def counts (counter, polymer):
    """Derive and return the counts of elements in `polymer` based only on
    the current dimer counts in `counter`.

    See also `counterize()`.
    """
    result = collections.Counter()

    for dimer in counter:
        result[ first(dimer) ] += counter[dimer]

    result[ last(polymer) ] += 1

    return result


def dimerize (rules):
    """Returns a new dictionary of `rules` that recasts each rule of the
    form:

         rules['AB'] = 'C'

    To the dimers each rule effectively produces with each
    polymerization reaction step:

        rules['AB'] = 'AC', 'CB'
    """
    return { d: (first(d) + rules[d], rules[d] + second(d)) for d in rules }


def dimers (polymer):
    """Iterate successive overlapping dimers (element pairs) in polymer."""

    # In Python 3.10 simply `return itertools.pairwise(polymer)`, which
    # is equivalent to creating two iterators from `polymer`, advancing
    # the second iterator by one (to discard the first element) and then
    # `zip()`ping the result:

    p1, p2 = itertools.tee(polymer)
    next(p2, None)
    yield from ( f'{d1}{d2}' for d1, d2 in zip(p1, p2) )


def first (dimer):
    """Returns the first element in `dimer`."""
    return dimer[0]


def last (polymer):
    """Returns the last element in `polymer`."""
    return polymer[-1]


def load (filename):
    """Loads template polymer and reaction rules from `filename`.  Returns
    `(template, rules)`.
    """
    rules = { }

    with open(filename) as stream:
        template, lines = stream.read().split('\n\n')

        for rule in lines.strip().split('\n'):
            pair, elem = rule.split(' -> ')
            rules[pair] = elem

    return template, rules


def polymerize (polymer, rules):
    """Polymerizes (expands) `polymer` according to `rules` and returns the
    newly formed polymer chain.
    """
    chain = [ ]

    for dimer in dimers(polymer):
        chain.append( first(dimer) )
        chain.append( rules[dimer] if dimer in rules else second(dimer) )

    chain.append( last(polymer) )

    return ''.join(chain)


def second (dimer):
    """Returns the second element in `dimer`."""
    return dimer[1]


filename        = 'aoc-2021-d14.txt'
template, rules = load(filename)


# Part 1
#
# Q: After 10 steps, difference between most and least common element counts?
# A: 10 Steps = 2010

polymer = template[:]

for step in range(10):
    polymer = polymerize(polymer, rules)

common = collections.Counter(polymer).most_common()
print(f'Part 1: 10 Steps = {common[0][1] - common[-1][1]}')


# Part 2
#
# Q: After 40 steps, difference between most and least common element counts?
# A: 40 Steps = 2437698971143

polymer  = template[:]
counter  = collections.Counter( dimer for dimer in dimers(polymer) )
rulemers = dimerize(rules)

for step in range(40):
    counter = counterize(counter, rulemers)

    if step + 1 == 10:
        common = counts(counter, polymer).most_common()
        print(f'Part 1: 10 Steps = {common[0][1] - common[-1][1]} (redux)')

common = counts(counter, polymer).most_common()
print(f'Part 2: 40 Steps = {common[0][1] - common[-1][1]}')
