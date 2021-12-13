#!/usr/bin/env python3

# Advent of Code 2021, Day 13 (https://adventofcode.com/2021/day/13)
# Author: Ben Bornstein


import collections
import itertools


def fold (paper, along, line, nrows, ncols):
    """Folds `paper` `along` (`'X'` or `'Y'`) axis at the horizontal or
    vertical `line`.  The size of `paper` is `nrows`-by-`ncols`.

    The `paper` is modified in-place (dots "below" or "right" of the
    fold are deleted and a new `(nrows, ncols)` paper size is returned.
    """

    # To reflect a point on the other side of a fold `line`:
    #
    #   1.  Compute point's distance below the fold line, e.g. (y - line)
    #   2.  Subtract that distance from the fold line, e.g. line - (y - line)
    #
    # That is, move the point up above the fold line the same distance
    # it was previously located down below the fold line.  For folds
    # along the x-axis, replace "below" with "right" and "y" with "x".

    if along == 'X':
        folded = lambda x, y: (line - (x - line), y)
        coords = itertools.product( range(line + 1, ncols), range(nrows) )
        size   = nrows, line
    else:
        folded = lambda x, y: (x, (line - (y - line)))
        coords = itertools.product( range(ncols), range(line + 1, nrows) )
        size   = line, ncols

    for coord in coords:
        if paper[coord]:
            paper[folded(*coord)] = True
            del paper[coord]

    return size


def load (filename):
    """Loads and returns `(paper, folds)` from `filename`."""
    paper = collections.defaultdict(bool)
    folds = None

    with open(filename) as stream:
        for line in stream.readlines():
            line = line.strip()

            if len(line) == 0:
                folds = [ ]
                continue

            if folds is None:
                x, y = map(int, line.split(','))
                paper[(x, y)] = True
            else:
                along, value = line.split('=')
                folds.append( (along[-1].upper(), int(value)) )

    return paper, folds


def pretty (paper, nrows, ncols, num_letters=8):
    """Pretty prints `paper` sized `nrows`-by-`ncols` with enough space for
    `num_letters` spaced apart to improve legibility.
    """
    char_width = ncols // num_letters

    for y in range(nrows):
        for char_start in range(0, ncols, char_width):
            for x in range(char_start, char_start + char_width):
                print('#' if paper[(x, y)] else ' ', end='')
            print('   ', end='')
        print()


def size (paper):
    """Returns the size of `paper` as `(nrows, ncols)`."""
    nrows = max(y for _, y in paper.keys()) + 1
    ncols = max(x for x, _ in paper.keys()) + 1
    return nrows, ncols



filename     = 'aoc-2021-d13.txt'
paper, folds = load(filename)
nrows, ncols = size(paper)


# Part 1
#
# Q: How many dots are visible after completing just the first fold?
# A: Count = 671

along, line  = folds[0]
nrows, ncols = fold(paper, along, line, nrows, ncols)

print(f'Part 1: Count = {sum( paper.values() )}')


# Part 2
#
# Q: What code do you use to activate ... camera system?
# A: PCPHARKL

for along, line in folds[1:]:
    nrows, ncols = fold(paper, along, line, nrows, ncols)

print(f'Part 2: ')
pretty(paper, nrows, ncols)
