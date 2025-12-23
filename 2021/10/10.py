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


def check_syntax(row):
    """Check syntax"""
    brackets = {'{': '}', '[': ']', '(': ')', '<': '>'}
    bracket_stack = []
    score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    for c in row:
        if c in ['{', '(', '[', '<']:
            #print("open")
            bracket_stack.append(c)
        elif c == brackets[bracket_stack[-1]]:
            bracket_stack.pop()
            #print("close")
        else:
            print(f"Wrong bracket {c}")
            return score[c]

    return 0


def check_incomplete(row):
    """Check incomplete lines"""
    brackets = {'{': '}', '[': ']', '(': ')', '<': '>'}
    bracket_stack = []
    score_table = {')': 1, ']': 2, '}': 3, '>': 4}
    for c in row:
        if c in ['{', '(', '[', '<']:
            #print("open")
            bracket_stack.append(c)
        elif c == brackets[bracket_stack[-1]]:
            bracket_stack.pop()
            #print("close")
        else:
            print(f"Wrong bracket {c}")
            return 0

    score = 0
    # Calculate incomplete line score
    while len(bracket_stack) > 0:
        score *= 5
        score += score_table[brackets[bracket_stack[-1]]]
        bracket_stack.pop()

    return score


def main():
    """Main program."""
    args = get_args()

    syntax_error_score = 0
    incomplete_list = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                if not args.second:
                    syntax_error_score += check_syntax(line.strip("\n\r"))
                else:
                    score = check_incomplete(line.strip("\n\r"))
                    if score > 0:
                        incomplete_list.append(score)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    if not args.second:
        print(f"Answer: {syntax_error_score}")
    else:
        incomplete_list.sort()
        print(incomplete_list)
        print(f"Answer: {incomplete_list[int(len(incomplete_list) / 2)]}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
