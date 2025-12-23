#!/usr/bin/env python3
"""
AdventOfCode day 16.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime


def get_args():
    """Parse args from terminal."""
    parser = argparse.ArgumentParser(
        description='AdventOfCode')
    parser.add_argument(
        '-i',
        '--input',
        help='Input file',
        required=True)

    parser.add_argument(
        '-s',
        '--second',
        help='Input file',
        action='store_true',
        default=False)

    return parser.parse_args()


class Packet:
    def __init__(self, bits):
        self.bits = bits
        self.length = len(bits)
        self.offset = 0
        self.version_sum = 0

    def read(self, n):
        """ Read n bits as int. """
        val = 0
        for i in range(n):
            val <<= 1
            if self.bits[self.offset + i] == '1':
                val |= 1
        self.offset += n
        return val

    def operation(self, op, values):
        """ Perform operation on values. """
        if op == 0:
            # sum
            result = 0
            for value in values:
                result += value
        elif op == 1:
            # product
            result = 1
            for value in values:
                result *= value
        elif op == 2:
            # minimum
            result = values[0]
            if len(values) > 1:
                for value in values[1:]:
                    if value < result:
                        result = value
        elif op == 3:
            # maximum
            result = values[0]
            if len(values) > 1:
                for value in values[1:]:
                    if value > result:
                        result = value
        elif op == 5:
            # greater than (always 2 values)
            if values[0] > values[1]:
                result = 1
            else:
                result = 0
        elif op == 6:
            # less than (always 2 values)
            if values[0] < values[1]:
                result = 1
            else:
                result = 0
        elif op == 7:
            # equal to (always 2 values)
            if values[0] == values[1]:
                result = 1
            else:
                result = 0

        return result

    def parse(self):
        """ Parse packet(s). """
        ver = self.read(3)
        self.version_sum += ver
        print(f"Version: {ver}")
        type_id = self.read(3)
        print(f"Packet type: {type_id}")
        if type_id == 4:
            # Parse literal value
            part = self.read(5)
            value = part & 0xf
            while part & 0x10 == 0x10:
                part = self.read(5)
                value <<= 4
                value |= part & 0xf
            print(f"Literal value: {value}")
            return value
        else:
            # Parse operator
            length_type_id = self.read(1)
            if length_type_id == 0:
                # 15 bit total sub packet length
                sub_packet_length = self.read(15)
                print(f"Sub packet(s) length: {sub_packet_length}")
                start_offset = self.offset
                values = []
                while self.offset - start_offset < sub_packet_length:
                    values.append(self.parse())
                return self.operation(type_id, values)
            else:
                sub_packets = self.read(11)
                print(f"Sub packets: {sub_packets}")
                values = []
                for _ in range(sub_packets):
                    values.append(self.parse())
                return self.operation(type_id, values)

    def align(self):
        """ Skip bits until next 4 bit alignment. """
        while self.offset & 4 != 0:
            self.offset += 1


def main():
    """Main program."""
    args = get_args()

    hex2bits = {'0': "0000", '1': "0001", '2': "0010", '3': "0011",
                '4': "0100", '5': "0101", '6': "0110", '7': "0111",
                '8': "1000", '9': "1001", 'A': "1010", 'B': "1011",
                'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"}
    bits = ""

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            line = line.strip("\n\r")
            for c in line:
                bits += hex2bits[c]

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(bits)
    packet = Packet(bits)
    # Parse packets
    answer = packet.parse()

    if not args.second:
        print(f"Answer: Version sum = {packet.version_sum}")
    else:
        print(f"Answer: {answer}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
