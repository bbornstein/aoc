#!/usr/bin/env python3

# Advent of Code 2021, Day 16 (https://adventofcode.com/2021/day/16)
# Author: Ben Bornstein


import collections
import functools
import operator


class Biterator:
    """Iterates over the bits in a given *string* of hexadecimal digits."""


    def __init__ (self, hexstring):
        """Creates a new `Biterator` over `hexstring`."""
        self._hexstring = hexstring
        self._position  = 0


    def __next__ (self):
        """Returns the next leftmost bit (`0` or `1`) in this `Biterator`'s
        `hexstring`.
        """
        nibble = self._position // 4

        if nibble > len(self._hexstring):
            raise StopIteration

        bit             = self._position %  4
        mask            = { 0: 0x8, 1: 0x4, 2: 0x2, 3: 0x1 }[bit]
        value           = (int(self._hexstring[nibble], base=16) & mask) != 0
        self._position += 1

        return int(value)


    @property
    def position (self):
        """The current bit position within this `Biterator`."""
        return self._position


    def next (self, nbits=1):
        """Returns the next leftmost `nbits` (as an integer) in this `Biterator`'s
        `hexstring`.
        """
        value = 0
        
        try:
            while nbits > 0:
                value  = (value << 1) | next(self)
                nbits -= 1
        except StopIteration:
            pass
        
        return value


Packet = collections.namedtuple('Packet', ['version', 'op', 'value'])


def evaluate (packet):
    """Evaluates Buoyancy Interchange Transmission System (BITS) `packet` and
    returns its value.
    """
    value = 0

    if packet.op == 0:
        value = sum(evaluate(p) for p in packet.value)
    
    elif packet.op == 1:
        value = functools.reduce(operator.mul, (evaluate(p) for p in packet.value), 1)
    
    elif packet.op == 2:
        value = min(evaluate(p) for p in packet.value)
    
    elif packet.op == 3:
        value = max(evaluate(p) for p in packet.value)
    
    elif packet.op == 4:
        value = packet.value
    
    elif packet.op == 5:
        value = int( evaluate(packet.value[0]) > evaluate(packet.value[1]) )

    elif packet.op == 6:
        value = int( evaluate(packet.value[0]) < evaluate(packet.value[1]) )
    
    elif packet.op == 7:
        value = int( evaluate(packet.value[0]) == evaluate(packet.value[1]) )

    return value


def parse (data):
    """Parses `data` and returns a corresponding Buoyancy Interchange Transmission
    System (BITS) `Packet`.
    
    The parameter `data` may be either a *string* of hexadecimal digits or a
    `Biterator`.
    """
    bits = data if type(data) is Biterator else Biterator(data)

    version  = bits.next(3)
    op       = bits.next(3)

    if op == 4:
        done  = False
        value = 0

        while not done:
            done   = bits.next(1) == 0
            value  = (value << 4) | bits.next(4)

    else:
        lengthid = bits.next(1)

        if lengthid == 0:
            nbits = bits.next(15)
            stop  = bits.position + nbits
            value = [ ]

            while bits.position < stop:
                value.append( parse(bits) )
            
            value = tuple(value)

        else:
            npackets = bits.next(11)
            value    = [ parse(bits) for p in range(npackets) ]

        value = tuple(value)

    return Packet(version, op, value)


def versions (packet):
    """Iterable over this packet's version and versions of all sub-packets."""
    yield packet.version
    
    if type(packet.value) is tuple:
        for p in packet.value:
            yield from versions(p)


# Part 1
#
# Q: What is the sum of the version numbers in all packets?
# A: Version Su == 31

assert parse('D2FE28')         == Packet(version=6, op=4, value=2021)
assert parse('38006F45291200') == Packet(version=1, op=6, value=(
                                      Packet(version=6, op=4, value=10),
                                      Packet(version=2, op=4, value=20) ))
assert parse('EE00D40C823060') == Packet(version=7, op=3, value=(
                                      Packet(version=2, op=4, value=1),
                                      Packet(version=4, op=4, value=2),
                                      Packet(version=1, op=4, value=3) ))

assert sum( versions( parse('8A004A801A8002F478')             ) ) == 16
assert sum( versions( parse('620080001611562C8802118E34')     ) ) == 12
assert sum( versions( parse('C0015000016115A2E0802F182340')   ) ) == 23
assert sum( versions( parse('A0016C880162017C3686B18A3D4780') ) ) == 31

filename = 'aoc-2021-d16.txt'

with open(filename) as stream:
    packet = stream.read().strip()

print(f'Version Sum = {sum( versions( parse(packet) ) )}')


# Part 2
#
# Q: Evaluate the expression represented by your hexadecimal-encoded BITS transmission?
# A: Result = 1392637195518

assert evaluate( parse('C200B40A82')                 ) ==  3
assert evaluate( parse('04005AC33890')               ) == 54
assert evaluate( parse('880086C3E88112')             ) ==  7
assert evaluate( parse('CE00C43D881120')             ) ==  9
assert evaluate( parse('D8005AC2A8F0')               ) ==  1
assert evaluate( parse('F600BC2D8F')                 ) ==  0
assert evaluate( parse('9C005AC2F8F0')               ) ==  0
assert evaluate( parse('9C0141080250320F1802104A08') ) ==  1

print(f'Result      = {evaluate( parse(packet) )}')
