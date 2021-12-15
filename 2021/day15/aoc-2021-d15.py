#!/usr/bin/env python3

# Advent of Code 2021, Day 15 (https://adventofcode.com/2021/day/15)
# Author: Ben Bornstein


import collections
import heapq


Point         = collections.namedtuple('Point', ['x', 'y'])
Point.__add__ = lambda self, q: Point(self[0] + q[0], self[1] + q[1])


class RiskMap:
    def __init__ (self):
        """Creates a new (empty) risk-level map.

        Individual risk-levels as specific positions are accessible via
        `RiskMap[Point]`.

        See also `RiskMap.load()`
        """
        self._factor = 1
        self._levels = [ ]
        self._nrows  = 0
        self._ncols  = 0


    def __getitem__ (self, pos):
        """Returns the risk-level at position `pos`, i.e. `RiskMap[pos]`."""
        if self._factor > 1:
            risk  = self._levels[pos.y % self._nrows][pos.x % self._ncols]
            risk += pos.y // self._nrows
            risk += pos.x // self._ncols

            if risk > 9:
                risk = risk % 9
        else:
            risk = self._levels[pos.y][pos.x]

        return risk


    @staticmethod
    def load (filename):
        """Creates a new risk-level map from `filename`."""
        rmap = RiskMap()

        with open(filename) as stream:
            for line in stream.readlines():
                rmap.append([ int(c) for c in line.strip() ])

        return rmap


    @property
    def ncols (self):
        """The number of columns in this `RiskMap`."""
        return self._factor * self._ncols


    @property
    def nrows (self):
        """The number of rows in this `RiskMap`."""
        return self._factor * self._nrows


    def append (self, row):
        """Appends `row` to this `RiskMap`."""
        if len(self._levels) == 0:
            self._ncols = len(row)

        self._levels.append(row)
        self._nrows += 1


    def neighbors (self, pos):
        """Iterable 4-neighbors (up, down, left, right) for `pos`ition."""
        deltas   = (-1, 0), (1, 0), (0, -1), (0, 1)
        adjacent = ( pos + Point(*delta) for delta in deltas )
        yield from ( p for p in adjacent if self.valid(p)    )


    def resize (self, factor):
        """Resizes this `RiskMap` by setting its expansion factor to `factor`
        copies both horizontally and vertically.
        """
        self._factor = factor


    def valid (self, pos):
        """Indicates whether or not `pos` is valid (inside this `RiskMap`)."""
        return pos.y in range(0, self.nrows) and pos.x in range(0, self.ncols)



def search (rmap, start, end):
    """Searches `RiskMap` `rmap` (breadth-first) to find the least risky
    path from `start` to `end`.  Returns the total risk of that path.
    """
    risk    = 0
    queue   = [ (rmap[p], p) for p in rmap.neighbors(start) ]
    visited = { start }

    heapq.heapify(queue)

    while len(queue) > 0:
        risk, current = heapq.heappop(queue)

        if current == end:
            break

        for pos in rmap.neighbors(current):
            if pos not in visited:
                heapq.heappush( queue, ((rmap[pos] + risk), pos) )
                visited.add(pos)

    return risk



filename = 'aoc-2021-d15.txt'
rmap     = RiskMap.load(filename)
start    = Point(0, 0)
end      = Point(rmap.nrows - 1, rmap.ncols - 1)


# Part 1
#
# Q: Lowest total risk of any path from the top left to the bottom right?
# A: Total Risk = 755

print(f'Part 1: Total Risk = {search(rmap, start, end):4}')


# Part 2
#
# Q: Lowest total risk of any path from the top left to the bottom right?
# A: Total Risk = 3016

rmap.resize(factor=5)
end = Point(rmap.nrows - 1, rmap.ncols - 1)

print(f'Part 2: Total Risk = {search(rmap, start, end)}')
