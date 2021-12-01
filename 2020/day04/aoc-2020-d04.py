#!/usr/bin/env python3

# Advent of Code 2020, Day 4 (https://adventofcode.com/2020/day/4)
# Author: Ben Bornstein


import re


class Passport (object):
    __slots__ = 'byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid', 'cid'
    Required  = 'byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid'

    def __init__ (self):
        """Creates a new empty Passport."""
        self.clear()


    def clear (self):
        """Clears all Passport fields."""
        for attr in Passport.__slots__:
            setattr(self, attr, None)


    def present (self):
        """Indicates whether all required fields are present."""
        return all(getattr(self, attr) != None for attr in Passport.Required)


    def update (self, line):
        """Updates Passport fields based on line, e.g.:

               ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        """
        for field in line.split():
            name, value = field.split(':')
            setattr(self, name, value)


    def valid (self):
        """Indicates whether all required fields are valid."""
        if not self.present():
            return False

        if re.match('\d{4}$', self.byr) is None:
            return False

        if int(self.byr) not in range(1920, 2002 + 1):
            return False

        if re.match('\d{4}$', self.iyr) is None:
            return False

        if int(self.iyr) not in range(2010, 2020 + 1):
            return False

        if re.match('\d{4}$', self.eyr) is None:
            return False

        if int(self.eyr) not in range(2020, 2030 + 1):
            return False

        match = re.match('(\d+)(cm|in)$', self.hgt)

        if match is None:
            return False

        if match[2] == 'cm' and int(match[1]) not in range(150, 193 + 1):
            return False

        if match[2] == 'in' and int(match[1]) not in range(59, 76 + 1):
            return False

        if re.match('#[0-9a-f]{6}$', self.hcl) is None:
            return False

        if self.ecl not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
            return False

        if re.match('\d{9}$', self.pid) is None:
            return False

        return True


# Part 1
#
# Q: In your batch file, how many passports are valid?
# A: Part 1: Valid passports: 237.

# Part 2
#
# Q: In your batch file, how many passports are valid?
# A: Part 2: Valid passports: 172.

filename = 'aoc-2020-d04.txt'
passport = Passport()
present  = 0
valid    = 0

with open(filename) as stream:
    for line in stream.readlines():
        line = line.strip()
        if len(line) == 0:
            present += int( passport.present() )
            valid   += int( passport.valid()   )
            passport.clear()
        else:
            passport.update(line)

present += int( passport.present() )
valid   += int( passport.valid()   )

print(f'Part 1: Valid passports: {present}.')
print(f'Part 2: Valid passports: {valid}.')
