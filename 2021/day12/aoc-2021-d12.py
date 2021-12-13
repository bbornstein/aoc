#!/usr/bin/env python3

# Advent of Code 2021, Day 12 (https://adventofcode.com/2021/day/12)
# Author: Ben Bornstein


import collections


def allowed_once (cave, visited):
    """Only allows small caves to be visited once.  Returns False if `cave`
    is small and already in `visited`.
    """
    return big(cave) or (small(cave) and cave not in visited)


def allowed_twice (cave, visited):
    """Only allows a single small cave to be visited twice.  Returns False
    if `cave` is small and any small cave is already in `visited` twice.
    """
    return big(cave) or (cave not in visited or (not twice(visited)))


def big (cave):
    """Indicates whether or not `cave` is big."""
    return cave.isupper()


def end (cave):
    """Indicates whether or not `cave` is 'end'."""
    return cave == 'end'


def load (filename):
    """Loads and returns a cave graph from `filename`.

    The returned cave graph will not contain the special 'start' node in
    any adjacency list since it's a source node.  Similarly the special
    'end' node will contain an empty adjacency list since it's a sink
    node.
    """
    caves = collections.defaultdict(list)

    with open(filename) as stream:
        for line in stream.readlines():
            src, dst = line.strip().split('-')

            if not start(dst):
                caves[src].append(dst)

            if not start(src) and not end(dst):
                caves[dst].append(src)

    return caves


def paths (caves, allowed):
    """Returns a count of all paths through `caves` graph according to
    `allowed` visit function.
    """
    count   = 0
    visited = [ ]

    def visit (caves, cave):
        nonlocal count
        visited.append(cave)

        for c in sorted(caves[cave]):
            if end(c):
                count += 1
            elif allowed(c, visited):
                visit(caves, c)
        visited.pop()

    for c in sorted(caves['start']):
        visit(caves, c)

    return count


def small (cave):
    """Indicates whether or not `cave` is small."""
    return cave.islower() and not (start(cave) or end(cave))


def start (cave):
    """Indicates whether or not `cave` is 'start'."""
    return cave == 'start'


def twice (visited):
    """Indicates whether or not any small cave as been visited twice.
    Returns True if any small cave is in `visited` twice.
    """
    return any(visited.count(cave) == 2 for cave in visited if small(cave))


filename = 'aoc-2021-d12.txt'
caves    = load(filename)


# Part 1
#
# Q: How many paths ... that visit small caves at most once?
# A: Paths = 5212

print(f'Part 1: Paths = {paths(caves, allowed_once):6}')


# Part 2
#
# Q: How many paths ... that visit once small cave at most twice?
# A:

print(f'Part 2: Paths = {paths(caves, allowed_twice)}')
