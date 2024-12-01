#!/usr/bin/env python3

# "Opens" an Advent of Code Puzzle for the given day.
# Author: Ben Bornstein


import argparse
import os
import sys


def system (cmd):
    print(cmd)
    os.system(cmd)


def write (filename, day):
    with open(filename, 'wt') as output:
        output.write(f"""#!/usr/bin/env python3

# Advent of Code 2024, Day {day} (https://adventofcode.com/2024/day/{day})
# Author: Ben Bornstein


def lines (filename, func=None):
    \"\"\"Python iterator over lines in `filename`.  If `func` is given, it is
    applied to each line before yielding (returning) it.
    \"\"\"
    with open(filename) as stream:
        for line in stream.readlines():
            yield func(line) if func else line


filename = 'aoc-2024-d{day:02}.txt'
data     = list( lines(filename) )


# Part 1
#
# Q:
# A:

print(f'Part 1: ')


# Part 2
#
# Q:
# A:

print(f'Part 2: ')
""")


def main ():
    """Opens an Advent of Code Puzzle for the given day."""
    p = argparse.ArgumentParser(description=main.__doc__)
    p.add_argument('day'   , type=int)
    p.add_argument('--year', type=int, default='2024')

    args      = p.parse_args()
    directory = f'day{args.day:02}'
    filename  = f'aoc-{args.year}-d{args.day:02}.py'
    pathname  = os.path.join(directory, filename)

    if not os.path.exists(directory):
        system(f'mkdir {directory}')
    else:
        print(f'Skipped creating {directory}.')

    if not os.path.exists(pathname):
        write(pathname, args.day)
        print(f'Wrote {pathname}.')
        system(f'chmod a+x {pathname}')
    else:
        print(f'Skipped writing {filename}.')


if __name__ == '__main__':
    sys.exit( main() )
