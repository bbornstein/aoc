#!/usr/bin/env python3

# Advent of Code 2020, Day 16 (https://adventofcode.com/2020/day/16)
# Author: Ben Bornstein


import functools
import re


def find (possible):
    """Returns `(key, index)` such that `possible[key] = [ index ]`."""
    for name, values in possible.items():
        if len(values) == 1:
            return name, values[0]

def flatten (array):
    """Returns a flattened array containing all elements of subarrays."""
    return [ elem for subarray in array for elem in subarray ]


def load (filename):
    """Loads and returns a dictionary of `rules` and list of `tickets` from
    filename.  The first ticket (`ticket[0]`) is "your ticket."
    """
    pattern = re.compile('([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)')
    state   = 'RULES'
    rules   = { }
    tickets = [ ]

    with open(filename) as stream:
        for line in stream.readlines():
            line = line.strip()

            if len(line) == 0:
                continue
            elif line == 'your ticket:' or line == 'nearby tickets:':
                state = 'TICKET'
                continue
            elif state == 'RULES':
                match = pattern.match(line)
                if match:
                    name        = match[1]
                    range1      = range( int(match[2]), 1 + int(match[3]) )
                    range2      = range( int(match[4]), 1 + int(match[5]) )
                    rules[name] = [ range1, range2 ]
            elif state == 'TICKET':
                tickets.append([ int(s) for s in line.split(',') ])

    return rules, tickets


def product (items):
    """Returns the product of the values in `items`."""
    return functools.reduce(lambda a, b: a * b, items, 1)


def remove (possible, value):
    """Removes value from all arrays in the `possible` dictionary."""
    for name, values in possible.items():
        try:
            del values[ values.index(value) ]
        except ValueError:
            pass


def transpose (tickets):
    """Returns the transpose of `tickets`, i.e. a grouping of fields for
    all `tickets`.
    """
    return zip(*tickets)


def valid (*args):
    """Indicates whether or not a `ticket` or one of its constituent
    `value`s is valid according to a single rule (`range1`, `range2`) or
    a dictionary of rules: `{ name1: (range1, range1), ..., nameN:
    (range1, range2) ]`.  That is, there are many ways to ask whether a
    `ticket` or one of its `value`s is valid:

        - valid(ticket, range1, range2)  # A rule is two Python range objects
        - valid(value , range1, range2)

    and:

        - valid(ticket, rules)
        - valid(value , rules)

    """
    result = False

    if len(args) == 2:
        obj    = args[0]
        rules  = args[1].values()
        result = any( valid(obj, range1, range2) for range1, range2 in rules )
    elif len(args) == 3:
        obj    = args[0]
        range1 = args[1]
        range2 = args[2]

        if type(obj) is int:
            value  = obj
            result = value in range1 or value in range2
        elif type(obj) is tuple or type(obj) is list:
            ticket = obj
            result = all( valid(value, range1, range2) for value in ticket )

    return result


# Part 1
#
# Consider the validity of the nearby tickets you scanned.
#
# Q: What is your ticket scanning error rate?
# A: Part 1: Ticket scanning error rate: 19060.

filename       = 'aoc-2020-d16.txt'
rules, tickets = load(filename)
errors         = [ v for v in flatten(tickets) if not valid(v, rules) ]

print(f'Part 1: Ticket scanning error rate: {sum(errors)}.')


# Part 2
#
# Once you work out which field is which, look for the six fields on
# your ticket that start with the word departure.
#
# Q: What do you get if you multiply those six values together?
# A: Part 2: Ticket "depature" product: 953713095011.

fields   = list( transpose([ t for t in tickets if valid(t, rules) ]) )
mapping  = { }
possible = { }


# Construct a list of possible (valid) mappings from rule names to field
# indexes.

for name, rule in rules.items():
    possible[name] = [ n for n, vs in enumerate(fields) if valid(vs, *rule) ]


# Iteratively reduce `possible` mappings by finding the first possible
# mapping that contains only a single field index.  Make that assignment
# permanent by:
#
#   1.  Adding `index` to `mapping`, and
#   2.  Removing `index` from all entries in `possible`
#
# Repeat until all `possible` mappings have been made permanent.

while len(possible) > 0:
    name, index   = find(possible)
    mapping[name] = index
    remove(possible, index)
    del possible[name]

ticket = tickets[0]
prefix = 'departure'
values = [ ticket[ mapping[key] ] for key in mapping if key.startswith(prefix) ]

print(f'Part 2: Ticket "depature" product: {product(values)}.')
