#!/usr/bin/env python3

# Advent of Code 2020, Day 19 (https://adventofcode.com/2020/day/19)
# Author: Ben Bornstein


def load (filename):
    """Loads and returns a dictionary of rules and a list of messages and
    returns `(rules, messages)`.
    """
    with open(filename) as stream:
        top, bottom = stream.read().split('\n\n')
        rules       = dict( parse(line) for line in top.split('\n') )
        messages    = bottom.strip().split('\n')

    return rules, messages


def match (msg, rules, rule=None):
    """Indicates whether or not `msg` matches `rule` in `rules`.  If `rule`
    is not specified, it defaults to `rules['0']`.
    """
    if rule is None:
        rule = rules['0']

    return matchPos(msg, 0, rules, rule) == len(msg)


def matchN (msg, pos, rules, rule, N):
    """Indicates whether or not `msg` matches `N` copies of `rule` in
    `rules`, starting at position `pos`.

    Returns the position in `msg` just after `N` successful matches, or
    -1 if no match was found.
    """
    for n in range(N):
        if (pos := matchPos(msg, pos, rules, rule)) == -1:
            break

    return pos


def matchPos (msg, pos, rules, rule):
    """Indicates whether or not `msg` matches `rule` in `rules`, starting at
    position `pos`.

    Returns the position in `msg` just after a successful match, or -1
    if no match was found.
    """
    index = -1

    if type(rule) is str:
        if rule.isdigit():
            index = matchPos(msg, pos, rules, rules[rule])
        elif msg[pos] == rule:
            index = pos + 1
    elif len(rule) > 0 and type(rule[0]) is list:
        index = matchPosAny(msg, pos, rules, rule)
    elif len(rule) > 0 and type(rule[0]) is str:
        index = matchPosAll(msg, pos, rules, rule)

    return index


def matchPosAll (msg, pos, rules, subrules):
    """Indicates whether or not `msg` matches all `subrule` in `rules`,
    starting at position `pos`.

    Returns the position in `msg` just after a successful match, or -1
    if no match was found.
    """
    index = pos

    for rule in subrules:
        if (index := matchPos(msg, index, rules, rule)) == -1:
            break

    return index


def matchPosAny (msg, pos, rules, subrules):
    """Indicates whether or not `msg` matches any (i.e. a single) `subrule`
    in `rules`, starting at position `pos`.

    Returns the position in `msg` just after a successful match, or -1
    if no match was found.
    """
    index = -1

    for rule in subrules:
        if (index := matchPos(msg, pos, rules, rule)) != -1:
            break

    return index


def match_42_31 (msg, rules):
    """Indicates whether or not `msg` matches the grammar in `rules`,
    starting with Rule 0 and the following "loop":

           0: 8 11
           8: 42 | 42 8
          11: 42 31 | 42 11 31

    which simplifies to:

           0: (42)^M (31)^N

    where M > N.
    """
    matched = False
    rule31  = rules['31']
    rule42  = rules['42']

    if (pos := matchN(msg, 0, rules, rule42, 1)) != -1:
        matches = int( len(msg) / pos )
        M       = (matches // 2) + 1

        while M < matches and matched is False:
            N       = matches - M
            pos     = 0
            match42 = (pos := matchN(msg, pos, rules, rule42, M)) != -1
            match31 = (pos := matchN(msg, pos, rules, rule31, N)) != -1
            matched = pos == len(msg) and match42 and match31
            M      += 1

    return matched


def parse (line):
    """Parses a rule line and returns `(rule, subrules)`."""
    rule, rhs = (s.strip() for s in line.split(':'))

    if rhs.count('"') == 2:
        subrules = rhs.replace('"', '')
    elif rhs.count('|') == 0:
        subrules = rhs.split()
    else:
        subrules = [ s.split() for s in rhs.split('|') ]

    return rule, subrules


filename        = 'aoc-2020-d19.txt'
rules, messages = load(filename)


# Part 1
#
# Q: How many messages completely match rule 0?
# A: Part 1: Messages matching Rule 0: 165.

matches = sum( int(match(msg, rules)) for msg in messages)
print(f'Part 1: Messages matching Rule 0: {matches}.')


# Part 2
#
# Q: After updating rules 8 and 11, how many messages match rule 0?
# A: Part 2: Messages matching Rule 0: (42)^M (31)^N: 274.

matches = sum( int(match_42_31(msg, rules)) for msg in messages)
print(f'Part 2: Messages matching Rule 0: (42)^M (31)^N: {matches}.')
