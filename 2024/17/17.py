#!/usr/bin/env python3
"""
AdventOfCode day 17.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import math
import operator


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


def do_next_operation(cpu):
    """Perform one instruction."""
    pc = cpu['PC']
    opcode = cpu['Program'][pc]
    operand = cpu['Program'][pc + 1]
    if operand < 4:
        combo_operand = operand
    elif operand == 4:
        combo_operand = cpu['A']
    elif operand == 5:
        combo_operand = cpu['B']
    elif operand == 6:
        combo_operand = cpu['C']

    if opcode == 0:
        # adv A = A / 2^combo_operand
        denominator = int(math.pow(2, combo_operand))
        print(f"adv: A = {cpu['A']} / {denominator}")
        cpu['A'] = cpu['A'] // denominator
        cpu['PC'] += 2
    elif opcode == 1:
        # bxl B = B ^ operand
        print(f"bxl: B = {cpu['B']} ^ {operand}")
        cpu['B'] = operator.xor(cpu['B'], operand)
        cpu['PC'] += 2
    elif opcode == 2:
        # bst B = combo_operand % 8
        print(f"bst: B = {cpu['B']} % {combo_operand}")
        cpu['B'] = combo_operand % 8
        cpu['PC'] += 2
    elif opcode == 3:
        # jnz NOP if A == 0, else PC = operand
        print(f"jnz")
        if cpu['A'] != 0:
            cpu['PC'] = operand
        else:
            cpu['PC'] += 2
    elif opcode == 4:
        # bxc B = B ^ C
        print(f"bxc: B = {cpu['B']} ^ {cpu['C']}")
        cpu['B'] = operator.xor(cpu['B'], cpu['C'])
        cpu['PC'] += 2
    elif opcode == 5:
        # out ouput value combo_operand % 8
        print(f"out")
        out = combo_operand % 8
        cpu['Output'].append(out)
        cpu['PC'] += 2
    elif opcode == 6:
        # bdv B = A / 2^combo_operand
        denominator = int(math.pow(2, combo_operand))
        print(f"bdv: B = {cpu['A']} / {denominator}")
        cpu['B'] = cpu['A'] // denominator
        cpu['PC'] += 2
    elif opcode == 7:
        # cdv C = A / 2^combo_operand
        denominator = int(math.pow(2, combo_operand))
        print(f"cdv: C = {cpu['A']} / {denominator}")
        cpu['C'] = cpu['A'] // denominator
        cpu['PC'] += 2


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

    cpu = {'A': 0, 'B': 0, 'C': 0, 'PC': 0, 'Program': [], 'Output': []}
    for line in lines:
        line = line.strip('\n')
        if len(line) == 0:
            continue
        if line.find("Register A") >= 0:
            cpu['A'] = int(line.split(':')[1])
        elif line.find("Register B") >= 0:
            cpu['B'] = int(line.split(':')[1])
        elif line.find("Register C") >= 0:
            cpu['C'] = int(line.split(':')[1])
        else:
            values = line.split(':')[1].split(',')
            for value in values:
                cpu['Program'].append(int(value))

    print(cpu)

    if args.second:
        print(f"")
    else:
        # Run program
        while cpu['PC'] < len(cpu['Program']):
            do_next_operation(cpu)
            print(cpu)

        str = ""
        for output in cpu['Output']:
            str += f"{output},"
        print(f"Program output: {str}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
