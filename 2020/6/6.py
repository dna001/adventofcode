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


def group_answer_count(group, everyone=False):
    """Count group answers."""
    answers = {}

    for line in group:
        for char in line.strip('\r\n'):
            if not char in answers:
                answers[char] = 0
            answers[char] += 1
            
    #print(line + '\n')
    print(answers)
    if not everyone:    
        return len(answers)

    correct_answers = 0
    print(len(group))
    for key, value in answers.items():
        if value == len(group):
            correct_answers += 1

    return correct_answers

def main():
    """Main program."""
    args = get_args()
    lines = []
    total_groups = 0
    groups_answer_sum = 0
    group = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                if len(line) > 0:
                    group.append(line)
                else:
                    groups_answer_sum += group_answer_count(group, args.second)
                    total_groups += 1
                    group = []
                line = file.readline()
            groups_answer_sum += group_answer_count(group, args.second)
            total_groups += 1

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print("Groups answer sum: {} ({})".format(groups_answer_sum, total_groups))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
