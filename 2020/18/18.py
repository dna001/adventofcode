#!/usr/bin/env python3
"""
AdventOfCode day 18.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
from pprint import pprint


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


def do_operand(a, b, op):
    """Perform operation."""
    val = a
    if op == '+':
        val += b
    elif op == '*':
        val *= b

    return val


def solve_calculation(line):
    """Solve calculation."""
    value_stack = []
    value_stack.append(0)
    operand_stack = []
    operand_stack.append('+')
    value = -1
    numbers = "0123456789"

    for char in line:
        if char == '(':
            value_stack.insert(0, 0)
            operand_stack.insert(0, '+')
        elif char == ')':
            if value > -1:
                #print(value_stack)
                #print(operand_stack)
                #print(value)
                value_stack[0] = do_operand(value_stack[0], value, operand_stack[0])
            val = value_stack.pop(0)
            operand_stack.pop(0)
            value_stack[0] = do_operand(value_stack[0], val, operand_stack[0])
            value = -1
        elif char == '+':
            operand_stack[0] = '+'
        elif char == '*':
            operand_stack[0] = '*'
        elif char in numbers:
            if value == -1:
                value = 0
            else:
                value *= 10
            value += int(char)
        elif char == ' ':
            if value > -1:
                #print(value_stack)
                #print(operand_stack)
                #print(value)
                value_stack[0] = do_operand(value_stack[0], value, operand_stack[0])
                value = -1
    if value > -1:
        value_stack[0] = do_operand(value_stack[0], value, operand_stack[0])

    return value_stack[0]


def main():
    """Main program."""
    args = get_args()

    answers = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            for line in file:
                line = line.strip('\n\r')
                val = solve_calculation(line)
                answers.append(val)
                print(val)

    except IOError:
        print("Failed reading file!")
        sys.exit()

    answer_sum = 0
    for answer in answers:
        answer_sum += answer

    print("Answer sum: {}".format(answer_sum))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
