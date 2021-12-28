#!/usr/bin/env python3

# Advent of Code 2021, Day 18 (https://adventofcode.com/2021/day/18)
# Author: Ben Bornstein


import collections
import itertools
import math


class SFNumber:
    """A Snailfish Number (`SFNumber`) is composed of a pair (list) of `SFNumber`s
    and/or `int`egers.  That is, each item in the pair may be another `SFNumber`
    or a regular `int`eger.

    Internally, `SFNumber`s track their `L`eft pair, `R`ight pair, `P`arent `SFNumber`
    (if any) or `None`, and their level of pair nesting.
    """

    def __init__ (self, pair, P=None, nested=0):
        """Creates a new `SFNumber` from `pair` and `reduce()`s it."""
        L           = pair[0]
        R           = pair[1]
        self.L      = SFNumber(L, self, nested + 1) if type(L) is list else L
        self.R      = SFNumber(R, self, nested + 1) if type(R) is list else R
        self.P      = P
        self.nested = nested

        if P is None:
            self.reduce()


    def __abs__ (self):
        """Returns the magnitude of this `SFNumber`."""
        L = self.L if type(self.L) is int else abs(self.L)
        R = self.R if type(self.R) is int else abs(self.R)
        return (3 * L) + (2 * R)


    def __add__ (self, other):
        """Adds this `SFNumber` to `other` `SFNumber`."""
        return SFNumber( [ self.list(), other.list() ] )


    def __eq__ (self, obj):
        """Tests this `SFNumber` for equality with `obj`, either another `SFNumber`
        or a Python nested `list` of pairs.
        """
        return self.list() == (obj.list() if type(obj) is SFNumber else obj)


    def __str__ (self):
        """Returns this `SFNumber` as a string showing a list of nested pairs."""
        return str( self.list() ).replace(' ', '')


    def explode (self):
        """Explodes the leftmost nested `SFNumber` once, if any.

        Returns `True` if a nested `SFNumber` exploded, `False` otherwise.
        """
        exploded = False

        for L, M, R in triples( self.inorder() ):
            if M.nested != 4:
                continue

            if L:
                if type(L.R) is int:
                    L.R += M.L
                elif type(L.L) is int:
                    L.L += M.L

            if R:
                if type(R.L) is int:
                    R.L += M.R
                elif type(R.R) is int:
                    R.R += M.R

            if M.P.L == M:
                M.P.L = 0
            elif M.P.R == M:
                M.P.R = 0

            exploded = True
            break

        return exploded


    def inorder (self):
        """Inorder iterator over the nested pairs of this `SFNumber`.
        
        Internal `SFNumber`s (with neither an integer left or right pair) are not
        iterated.
        """
        if type(self.L) is not int:
            yield from self.L.inorder()

        if type(self.L) is int or type(self.R) is int:
            yield self

        if type(self.R) is not int:
            yield from self.R.inorder()


    def list (self):
        """Returns this `SFNumber` as a Python `list` of nested pairs."""
        L = self.L if type(self.L) is int else self.L.list()
        R = self.R if type(self.R) is int else self.R.list()
        return [L, R]


    def split (self):
        """Splits the leftmost nested `SFNumber` once, if any.
        
        Returns `True` if a nested `SFNumber` split, `False` otherwise.
        """
        pair = None

        for n in self.inorder():
            if type(n.L) is int and n.L >= 10:
                pair = [ math.floor(n.L/2), math.ceil(n.L/2) ]
                n.L  = SFNumber(pair, n, n.nested + 1)

            elif type(n.R) is int and n.R >= 10:
                pair = [ math.floor(n.R/2), math.ceil(n.R/2) ]
                n.R  = SFNumber(pair, n, n.nested + 1)

            if pair:
                break

        return pair is not None


    def reduce (self):
        """Reduces this `SFNumber` in place."""
        while self.explode() or self.split():
            pass




def load (filename):
    """Loads a list of Snailfish numbers (`SFNumber`s) from `filename`."""
    with open(filename) as stream:
        return read( stream.read().strip() )


def read (lines):
    """Reads and returns a list of Snailfish numbers (`SFNumber`s) from `lines`."""
    return [ SFNumber( eval(line) ) for line in lines.split('\n') ]


def triples (iterable):
    """Iterates over `iterable` in 3-tuples including `(None, first, second)` and
    `(penultimate, last, None)`.
    """
    it       = iter(iterable)
    triplets = collections.deque(itertools.islice(it, 2), maxlen=3)
    triplets.appendleft(None)

    if len(triplets) == 3:
        yield tuple(triplets)

    for item in it:
        triplets.append(item)
        yield tuple(triplets)
    
    triplets.append(None)
    yield tuple(triplets)



assert SFNumber( [[[[[9,8],1],2],3],4] ) == [[[[0,9],2],3],4]
assert SFNumber( [7,[6,[5,[4,[3,2]]]]] ) == [7,[6,[5,[7,0]]]]
assert SFNumber( [[6,[5,[4,[3,2]]]],1] ) == [[6,[5,[7,0]]],3]

n = SFNumber( [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] )
assert n == [[3,[2,[8, 0]]],[9,[5,[7,0]]]]

n = SFNumber( [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] )
assert n == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

n = SFNumber( [[[[4,3],4],4],[7,[[8,4],9]]] ) + SFNumber( [1,1] )
assert n == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

numbers = read('[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]')
assert sum(numbers[1:], start=numbers[0]) == [[[[5,0],[7,4]],[5,5]],[6,6]]


filename = 'aoc-2021-d18.txt'
numbers  = load(filename)


# Part 1
#
# Q: What is the magnitude of the final sum?
# A: Magnitude = 4132

print(f'Magnitude     = {abs( sum(numbers[1:], start=numbers[0]) )}')


# Part 2
#
# Q: What is the largest magnitude of any sum of two different snailfish numbers?
# A: Max Magnitude = 4685


m = max( abs(m + n) for m, n in itertools.permutations(numbers, 2) )
print(f'Max Magnitude = {m}' )