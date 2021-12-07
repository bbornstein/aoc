#! /usr/bin/env gforth

\ Advent of Code 2021, Day 2 (https://adventofcode.com/2021/day/2)
\ Author: Ben Bornstein


\ The problem description uses "depth" but to avoid redefining such a
\ fundamental Forth word (the number of values on the data stack), we use
\ "deep".

\ The word mag(nitude) reads from input stream and places the value on
\ the data stack.  This code is taken directly from "Starting Forth",
\ Chapter 10 "I/O and You" under the section "Number Input Conversion".
\
\ See https://www.forth.com/starting-forth/10-input-output-operators

variable aim
variable deep
variable pos

: mag    ( -- n ) 0. bl word count >number 2drop drop ;
: report ( -- )   pos @ . ." pos * " deep @ . ." depth = " pos @ deep @ * . cr ;
: reset  ( -- )   0 aim ! 0 deep ! 0 pos ! ;


\ Part 1
\
\ Q: Multiply your final horizontal position by your final depth?
\ A: Part 1: 1925 pos * 879 depth = 1692075

: forward ( -- ) mag pos  +! ;
: down    ( -- ) mag deep +! ;
: up      ( -- ) deep @ mag - deep ! ;

reset
include aoc-2021-d02.txt
." Part 1: " report


\ Part 2
\
\ Q: Multiply your final horizontal position by your final depth?
\ A: Part 2: 1925 pos * 908844 depth = 1749524700

: forward ( -- ) mag dup pos +! aim @ * deep +! ;
: down    ( -- ) mag aim +! ;
: up      ( -- ) aim @ mag - aim ! ;

reset
include aoc-2021-d02.txt
cr ." Part 2: " report

bye
