#!/usr/bin/env python3

# Advent of Code 2020, Day 7 (https://adventofcode.com/2020/day/7)
# Author: Ben Bornstein


import re


class Bag (object):
    """Bags have a `color` and quantity (`qty`).

    A Bag's allowed quantity (`qty`) is really a property of containing
    (parent) `bag`, but it's most convenient to store on a Bag itself.
    Bag (objects) are lightweight (pun intended) and only a Bag's
    `color` is used for the purposes of identity (equality and hashing),
    i.e.:

        Bag('1 shiny gold bag') == Bag('2 shiny gold bags'), and so on.
    """
    __slots__ = 'color', 'qty'
    Pattern   = re.compile('(\d+)?\s?(\w+ \w+)\s?(bag|bags)?\.?')

    def __init__ (self, desc):
        """Creates a new Bag based on a string description with many variations
        on a theme (see Bag.Pattern regular expression), e.g.:

             - shiny gold
             - vibrant plum bag
             - 2 dark orange bags
        """
        match      = Bag.Pattern.search(desc)
        self.color = match[2]
        self.qty   = int( match[1] ) if match[1] else 0

    def __eq__ (self, other):
        return self.color == other.color

    def __hash__ (self):
        return hash(self.color)

    def __str__ (self):
        return self.color


def bags (graph, bag):
    """Return the number of bags that `bag` can contain."""
    if len( graph[bag] ) == 0:
        return 0
    else:
        return sum(b.qty + (b.qty * bags(graph, b)) for b in graph[bag])


def contains (graph, bag, bags):
    """Indicates whether `bag` is (eventually) in `bags` (or its bags)."""
    return bag in bags or any(contains(graph, bag, graph[b]) for b in bags)


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def parse (line):
    """Parses line and returns a tuple of `(bag, contents)` where `bag` is a
    `Bag` and `contents` is a list of `Bag`s that `bag` contains.
    """
    node, rest = line.strip().split(' contain ', 2)
    return Bag(node), [ Bag(s) for s in rest.split(', ') ]


# Part 1
#
# Q: How many bag colors can contain at least one shiny gold bag?
# A: Part 1: Bag colors containing a shiny gold bag: 259.

bag          = Bag('shiny gold')
empty        = Bag('no other')
filename     = 'aoc-2020-d07.txt'
graph        = { bag: contents for bag, contents in lines(filename, parse) }
graph[empty] = [ ]

colors = set(b for b in graph if contains(graph, bag, graph[b]))
print(f'Part 1: Bag colors containing a {bag} bag: {len(colors)}.')


# Part 2
#
# Q: How many bags are required inside your single shiny gold bag?
# A: Part 2: Bags required inside shiny gold bag: 45018.

print(f'Part 2: Bags required inside {bag} bag: {bags(graph, bag)}.')
