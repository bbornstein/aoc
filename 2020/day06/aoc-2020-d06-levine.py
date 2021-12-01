#!/usr/bin/env python3

# Advent of Code 2020, Day 6 (https://adventofcode.com/2020/day/6)
# Author: Paul A. Levine (329F) <Paul.A.Levine@jpl.nasa.gov>


# Part 1
#
# Q: For each group, count the number of questions to which anyone
# answered "yes".  What is the sum of those counts?
# A: Part 1: Sum of counts: 6351.

# Part 2
#
# Q: For each group, count the number of questions to which everyone
# answered "yes".  What is the sum of those counts?
# A: Part 2: Sum of counts: 3143.

filename  = 'aoc-2020-d06.txt'
anyone    = 0
everyone  = 0

with open(filename) as stream:
    text = stream.read()

for group in text.split('\n\n'):
    people    = [ set(person) for person in group.split() ]
    anyone   += len( set.union(*people) )
    everyone += len( set.intersection(*people) )

print(f'Part 1: Sum of counts: {anyone}.')
print(f'Part 2: Sum of counts: {everyone}.')
