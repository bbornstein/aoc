#!/bin/bash

# Advent of Code 2023, Day 1 (https://adventofcode.com/2023/day/1)
# Author: Ben Bornstein


# Part 1
#
# Q: What is the sum of all of the calibration values?
# A: Part 1: The sum of all calibration values is 54708

echo -n "Part 1: The sum of all calibration values is "

cat aoc-2023-d01.txt   \
    | sed 's/[a-z]//g' \
    | sed -E 's/([0-9])[0-9]*([0-9])/\1\2/' \
    | sed -E 's/^([0-9])$/\1\1/'            \
    | awk '{sum += $1;} END {print sum;}'


# Part 2
#
# Q: What is the sum of all of the calibration values?
# A: Part 2: The sum of all calibration values is 54087

echo -n "Part 2: The sum of all calibration values is "

cat aoc-2023-d01.txt    \
  | sed 's/one/o1e/g'   \
  | sed 's/two/t2o/g'   \
  | sed 's/three/t3e/g' \
  | sed 's/four/f4r/g'  \
  | sed 's/five/f5e/g'  \
  | sed 's/six/s6x/g'   \
  | sed 's/seven/s7n/g' \
  | sed 's/eight/e8t/g' \
  | sed 's/nine/n9e/g'  \
  | sed 's/[a-z]//g'    \
  | sed -E 's/([0-9])[0-9]*([0-9])/\1\2/' \
  | sed -E 's/^([0-9])$/\1\1/'            \
  | awk '{sum += $1;} END {print sum;}'
