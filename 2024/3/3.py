#!/usr/bin/env python3
"""
AdventOfCode day 3.
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


def main():
    """Main program."""
    args = get_args()

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    code = ""
    for line in lines:
        line = line.strip('\n')
        code += line

    if args.second:
        sum = 0
        pos = 0
        mul_enabled = True
        while(pos >= 0 and pos < len(code)):
            val1 = 0
            val2 = 0
            val1_found = False
            val2_found = False
            if mul_enabled:
                dont_pos = code.find("don't()", pos)
                mul_pos = code.find("mul(", pos)
                if dont_pos > 0 and dont_pos < mul_pos:
                    mul_enabled = False
                    pos = dont_pos
                    print("Found don't()")
                    continue
                pos = mul_pos
                print(pos)
                if pos < 0:
                    break
                pos += 4
                # Digit 1
                while(True):
                    if code[pos].isdigit():
                        val1 = val1 * 10 + int(code[pos])
                        pos += 1
                        val1_found = True
                    else:
                        break
                if not val1_found:
                    continue
                if code[pos] == ',':
                    pos += 1
                else:
                    continue
                # Digit 2
                while(True):
                    if code[pos].isdigit():
                        val2 = val2 * 10 + int(code[pos])
                        pos += 1
                        val2_found = True
                    else:
                        break
                if not val2_found:
                    continue
                if code[pos] == ')':
                    pos += 1
                    print(f"Found mul ({val1} * {val2})")
                    sum += val1 * val2
                else:
                    continue
            else:
                pos = code.find("do()", pos)
                if pos > 0:
                    mul_enabled = True
                    print("Found do()")
                    continue

        print(f'Sum of mul instructions: {sum}')

    else:
        sum = 0
        pos = 0
        while(pos < len(code)):
            val1 = 0
            val2 = 0
            val1_found = False
            val2_found = False
            pos = code.find("mul(", pos)
            print(pos)
            if pos < 0:
                break
            pos += 4
            # Digit 1
            while(True):
                if code[pos].isdigit():
                    val1 = val1 * 10 + int(code[pos])
                    pos += 1
                    val1_found = True
                else:
                    break
            if not val1_found:
                continue
            if code[pos] == ',':
                pos += 1
            else:
                continue
            # Digit 2
            while(True):
                if code[pos].isdigit():
                    val2 = val2 * 10 + int(code[pos])
                    pos += 1
                    val2_found = True
                else:
                    break
            if not val2_found:
                continue
            if code[pos] == ')':
                pos += 1
                print(f"Found mul ({val1} * {val2})")
                sum += val1 * val2
            else:
                continue

        print(f'Sum of mul instructions: {sum}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
