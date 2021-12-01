#!/usr/bin/env python3

# Advent of Code 2020, Day 8 (https://adventofcode.com/2020/day/8)
# Author: Ben Bornstein


import collections


ACC, JMP, NOP = 1, 2, 3
Opcodes       = { 'acc': ACC, 'jmp': JMP, 'nop': NOP }
Instruction   = collections.namedtuple('Instruction', 'op arg')


def flip (ins):
    """Flips a `JMP` `ins`truction to a `NOP`, or vice-versa."""
    return ins._replace(op=JMP if ins.op == NOP else NOP)


def halts (program):
    """Indicates whether or not `program` halts (True) or loops forever
    (False).  This function also returns the state of the program
    (accumulator) at the point it terminates or loops, i.e.:

        (halted=True | False, accumulator)
    """
    acc    = 0
    exe    = set()
    pc     = 0
    halted = True

    while pc < len(program):
        if pc in exe:
            halted = False
            break

        exe.add(pc)
        ins = program[pc]

        if ins.op == JMP:
            pc += ins.arg
        else:
            if ins.op == ACC:
                acc += ins.arg
            pc += 1

    return halted, acc


def lines (filename, func=None):
    """Python iterator over lines in filename.  If func is given, it is
    applied to each line before yielding (returning) it.
    """
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


def parse (line):
    """Parses a program line, returning `(opcode, argument)`."""
    op, arg = line.split()
    return Instruction(Opcodes.get(op), int(arg))


filename = 'aoc-2020-d08.txt'
program  = list( lines(filename, parse) )


# Part 1
#
# Run your copy of the boot code.
#
# Q: Before any instruction is executed a second time, what is the accumulator?
# A: Part 1: Loop detected: acc=1859.

halted, acc = halts(program)

if not halted:
    print(f'Part 1: Loop detected: acc={acc}.')


# Part 2
#
# Fix the program so that it terminates normally by changing exactly one
# jmp (to nop) or nop (to jmp).
#
# Q: What is the value of the accumulator after the program terminates?
# A: Part 2: Program terminated: acc=1235.

for n in range( len(program) ):
    if program[n].op == ACC:
        continue

    program[n]  = flip( program[n] )
    halted, acc = halts(program)
    program[n]  = flip( program[n] )

    if halted:
        print(f'Part 2: Program terminated: acc={acc}.')
        break
