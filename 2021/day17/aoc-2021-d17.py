#!/usr/bin/env python3

# Advent of Code 2021, Day 17 (https://adventofcode.com/2021/day/17)
# Author: Ben Bornstein

#        1                   2         3         4         5         6         7
#2345678901234567890123456789012345678901234567890123456789012345678901234567890123456789


import collections
import itertools
import re


Position = collections.namedtuple('Position', ['x', 'y'])
Velocity = collections.namedtuple('Velocity', ['x', 'y'])


class Probe:
    """Probes keep track of their `pos`ition, `vel`ocity and maximum `height`."""

    def __init__ (self, vx, vy):
        """Creates a new `Probe` with initial velocity `vx` and `vy`."""
        self.height = 0
        self.pos    = Position(0, 0)
        self.vel    = Velocity(vx, vy)


    def launch (self, target):
        """Launches this `Probe` toward `target`.
        
        This `Probe` continues until it either hits or decidedly misses the `target`.
        Returns True if `target` is hit, False if `target` is missed.
        """
        hit = self.pos in target

        while not hit and not target.missed(self):
            self.step()
            hit = self.pos in target

        return hit


    def step (self):
        """Steps this `Probe`'s position according to its velocity and adjusts its
        subsequent velocity for drag.
        """
        self.pos    = Position(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        self.vel    = Velocity(self.vel.x - sign(self.vel.x), self.vel.y - 1)
        self.height = max(self.height, self.pos.y)



class Target (collections.namedtuple('Target', ['xrange', 'yrange'])):
    """Targets are defined by an `xrange` and `yrange`."""

    @staticmethod
    def load (filename):
        """Loads and returns a `Target` from `filename`."""
        with open(filename) as stream:
            return Target.read( stream.read().strip() )


    @staticmethod
    def read (desc):
        """Reads and returns a `Target` from a single line `desc`ription."""
        match = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', desc)
        xmin, xmax, ymin, ymax = [ int(m) for m in match.groups() ]

        return Target( range(xmin, xmax + 1), range(ymin, ymax + 1) )


    def __contains__ (self, pos):
        """Indicates whether or not `pos` is contain in this `Target`."""
        return pos.x in self.xrange and pos.y in self.yrange 


    def missed (self, probe):
        """Indicates whether or not `probe` decidedly missed this `Target`."""
        return probe.pos.x > self.xrange.stop or probe.pos.y < self.yrange.start


def sign (x):
    """Returns the sign of `x` as `-1`, `0`, or `+1`.""" 
    return 0 if x == 0 else +1 if x > 0 else -1


filename = 'aoc-2021-d17.txt'
# target = Target.read('target area: x=20..30, y=-10..-5')
target   = Target.load(filename)
height   = 0
count    = 0

for vx, vy in itertools.product( range(0, target.xrange.stop), range(-100, 100) ):
    probe = Probe(vx, vy)

    if probe.launch(target):
        count += 1
        height = max(height, probe.height)


# Part 1
#
# Q: What is the highest y position it reaches on this trajectory?
# A: Height = 4656

print(f'Part 1: Height     = {height}')


# Part 2
#
# Q: How many distinct initial velocities cause the probe to hit the target?
# A: Velocities = 1908

print(f'Part 2: Velocities = {count}')
