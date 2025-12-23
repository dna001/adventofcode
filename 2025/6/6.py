#!/usr/bin/env python3
"""
AdventOfCode day 6.
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

        
    if args.second:
        values = []
        operators = ""
        for line in lines:
            tmp = line.strip('\n')
            if tmp[0] == '*' or tmp[0] == '+':
                operators = tmp
            else:
                values.append(tmp)

        print(values)
        print(operators)
        answer = 0
        offset = len(operators) - 1
        new_values = []
        while offset >= 0:
            value = -1
            for row in values:
                if row[offset] != ' ':
                    if value < 0:
                        value = int(row[offset])
                    else:
                        value = value * 10 + int(row[offset])
            if value >= 0:
                print(value)
                new_values.append(value)

            if operators[offset] == '*':
                a = 1
                for v in new_values:
                    a *= v
                print(a)
                answer += a
                new_values = []

            elif operators[offset] == '+':
                a = 0
                for v in new_values:
                    a += v
                print(a)
                answer += a
                new_values = []

            offset -= 1

        print(f'Answer {answer}')
    else:
        values = []
        operators = ""
        for line in lines:
            tmp = line.strip('\n')
            if tmp[0] == '*' or tmp[0] == '+':
                for t in tmp:
                    if t == '*' or t == '+':
                        operators += t
            else:
                row = []
                tmp = tmp.split(' ')
                for t in tmp:
                    if len(t) > 0:
                        row.append(int(t))
                
                values.append(row)

        print(values)
        print(operators)
        answer = 0
        for i in range(len(operators)):
            if operators[i] == '*':
                value = 1
            else:
                value = 0
            for row in values:
                if operators[i] == '*':
                    value *= row[i]
                elif operators[i] == '+':
                    value += row[i]
            print(value)
            answer += value

        print(f'Answer {answer}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
