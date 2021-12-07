#!/usr/bin/env python3

# Advent of Code 2021, Day 4 (https://adventofcode.com/2021/day/4)
# Author: Ben Bornstein

import itertools


def card (lines):
    """Creates a bingo card (matrix) from `lines`."""
    lines = lines.strip().split('\n')
    return [ [ int(s) for s in line.split() ] for line in lines ]


def load (filename):
    """Loads a bingo game from `filename` and returns `(numbers, boards)`."""
    with open(filename) as stream:
        numbers = [ int(s) for s in stream.readline().split(',') ]
        discard = stream.readline()
        boards  = [ card(lines) for lines in stream.read().split('\n\n') ]

    return numbers, boards


def mark (board, draw):
    """Marks the bingo `board` with the number `draw`."""
    nrows = len( board    )
    ncols = len( board[0] )

    for row, col in itertools.product( range(nrows), range(ncols) ):
        if board[row][col] == draw:
            board[row][col] = 'x'


def score (board, draw):
    """Scores the bingo `board`, including the last `draw`."""
    return sum(s for s in itertools.chain(*board) if s != 'x') * draw


def winner (board):
    """Indicates whether or not this bingo `board` is a winner."""
    done = lambda squares: all(s == 'x' for s in squares)
    return any(done(row) or done(col) for row, col in zip(board, zip(*board)))


filename        = 'aoc-2021-d04.txt'
numbers, boards = load(filename)
scores          = [ ]

for draw, board in itertools.product(numbers, boards):
    if not winner(board):
        mark(board, draw)
        if winner(board):
            scores.append( score(board, draw) )
            if len(scores) == len(boards):
                break


# Part 1
#
# Q: What will your final score be if you choose that board?
# A: Score = 12796

print(f'Part 1: Score = {scores[0]}')


# Part 2
#
# Q: Once it wins, what would its final score be?
# A: Score = 18063

print(f'Part 2: Score = {scores[-1]}')
