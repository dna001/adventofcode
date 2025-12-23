#!/usr/bin/env python3
"""
AdventOfCode day 10.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import math
import copy

sum_of_total_sizes = 0

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


def execute_cycle(state):
    """ Execute one cycle in the CPU. """

    state['cycle_count'] += 1
    state['instr_cycle'] += 1

    # Check state during the cycle x
    if (state['cycle_count'] - 20) % 40 == 0:
        signal_strength = state['cycle_count'] * state['reg_x']
        #print(f"instr: {state['instr']}, instr_val: {state['instr_val']}, instr_cycle: {state['instr_cycle']}")
        #print(f"cycle_count: {state['cycle_count']}, reg_x: {state['reg_x']}")
        #print(f"Signal strength at {state['cycle_count']}: {signal_strength}")
        state['signal_strength_sum'] += signal_strength

    # Draw in pixel matrix
    if (state['cycle_count'] - 1) % 40 in range(state['reg_x'] - 1, state['reg_x'] + 2):
        state['pixel_matrix'] += '#'
    else:
        state['pixel_matrix'] += '.'

    instr_done = False
    if state['instr'] == 'addx':
        if state['instr_cycle'] == 2:
            state['reg_x'] += state['instr_val']
            instr_done = True
    elif state['instr'] == 'noop':
        instr_done = True

    return instr_done


def main():
    """Main program."""
    args = get_args()
    cpu_state = {'cycle_count': 0, 'reg_x': 1, 'instr': None, 'instr_val': 0, 'instr_cycle': 0,
                 'signal_strength_sum': 0, 'pixel_matrix': ""}

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline().strip('\n')
            while line:
                if 'addx' in line:
                    cpu_state['instr'] = 'addx'
                    cpu_state['instr_val'] = int(line.split(' ')[1])
                    cpu_state['instr_cycle'] = 0
                elif 'noop' in line:
                    cpu_state['instr'] = 'noop'
                    cpu_state['instr_val'] = 0
                    cpu_state['instr_cycle'] = 0
                instr_done = False
                while not instr_done:
                    instr_done = execute_cycle(cpu_state)

                line = file.readline().strip('\n')

    except IOError:
        print("Failed reading file!")
        sys.exit()

    if args.second:
        for row in range(0, 6):
            print(f"{cpu_state['pixel_matrix'][row * 40: row * 40 + 40]}")
    else:
        print(f"Signal strength sum; {cpu_state['signal_strength_sum']}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
