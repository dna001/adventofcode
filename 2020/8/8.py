#!/usr/bin/env python3
"""
AdventOfCode day 8.
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


def run_program(program):
    """Run program."""
    acc = 0
    cycles = 0
    pc = 0
    pc_hits = []

    while pc >= 0 and pc < len(program) and not program[pc]['visited']:
        opcode = program[pc]['opcode']
        value = program[pc]['value']

        program[pc]['visited'] = True
        if opcode == 'acc':
            acc += value
            pc += 1
        if opcode == 'nop':
            pc += 1
        if opcode == 'jmp':
            pc += value
        cycles += 1

    return (pc == len(program), acc, cycles)

def main():
    """Main program."""
    args = get_args()
    total_lines = 0
    program = []
    pc = 0
    accumulator = 0
    cycles = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                program.append({'opcode': line.split(' ')[0], 'value': int(line.split(' ')[1])})
                total_lines += 1
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(program)

    if not args.second:
        while program[pc]['opcode'] != 'brk':
            opcode = program[pc]['opcode']
            value = program[pc]['value']

            program[pc]['opcode'] = 'brk'
            if opcode == 'acc':
                accumulator += value
                pc += 1
            if opcode == 'nop':
                pc += 1
            if opcode == 'jmp':
                pc += value
            cycles += 1

        print("Accumulator is {} when infinite loop starts (pc {} cycles {})".format(accumulator, pc, cycles))
    else:
        for addr in range(0, len(program)):
            old_opcode = None
            if program[addr]['opcode'] == 'nop':
                old_opcode = 'nop'
                program[addr]['opcode'] = 'jmp'
            elif program[addr]['opcode'] == 'jmp':
                old_opcode = 'jmp'
                program[addr]['opcode'] = 'nop'

            for instr in program:
                instr['visited'] = False
            (res, accumulator, cycles) = run_program(program)
            print("res: {} acc: {} cycles: {}".format(res, accumulator, cycles))

            if res:
                break

            if old_opcode:
                program[addr]['opcode'] = old_opcode

        print("Accumulator is {} when program terminates (cycles {} addr {})".format(accumulator, cycles, addr))
    #input("Press any key to continue...")

if __name__ == "__main__":
    main()
