#!/usr/bin/env python3
"""
AdventOfCode day 14.
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


def count_after_x_steps(pair, steps, rules):
    """Count occurenses for pair after x steps."""
    polymer_template = pair
    print(f"rule: {pair}")
    for step in range(1, steps + 1):
        new_polymer_template = ""
        for n in range(0, len(polymer_template) - 1):
            new_polymer_template += polymer_template[n] + rules[polymer_template[n: n + 2]]
        new_polymer_template += polymer_template[-1]
        polymer_template = new_polymer_template
        print(f"After step {step}: {len(polymer_template)}")

    #Count occurens
    count_bins = {}
    for c in polymer_template:
        if c in count_bins.keys():
            count_bins[c] += 1
        else:
            count_bins[c] = 1
    print(count_bins)

    return {'template': polymer_template, 'bin_count': count_bins}


def sum_bins(dst_bin, src_bin):
    """Sum of 2 count bins."""
    for key, value in src_bin.items():
        if key in dst_bin.keys():
            dst_bin[key] += value
        else:
            dst_bin[key] = value


def count_after_40_steps(rule, count_per_rule):
    """Count after 40 steps using precalculated count bins."""
    count_bins = {}
    template = count_per_rule[rule]['template']
    for n in range(0, len(template) - 1):
        sum_bins(count_bins, count_per_rule[template[n:n + 2]]['bin_count'])
        # Remove rightmost char
        rightmost_char = count_per_rule[template[n:n + 2]]['template'][-1]
        count_bins[rightmost_char] -= 1
    # Add one count for rightmost char
    #count_bins[template[-1]] += 1

    return count_bins


def main():
    """Main program."""
    args = get_args()

    pair_insertion_rules = {}

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            polymer_template = line.strip("\n\r")
            file.readline()
            line = file.readline()
            while line:
                pair = line.strip("\n\r").split(' -> ')
                pair_insertion_rules[pair[0]] = pair[1]
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(f"Template: {polymer_template}")
    print(pair_insertion_rules)

    if not args.second:
        for step in range(1, 11):
            new_polymer_template = ""
            for n in range(0, len(polymer_template) - 1):
                new_polymer_template += polymer_template[n] + pair_insertion_rules[polymer_template[n: n + 2]]
            new_polymer_template += polymer_template[-1]
            polymer_template = new_polymer_template
            print(f"After step {step}: {len(polymer_template)}")

        #Count occurens
        count_bins = {}
        for c in polymer_template:
            if c in count_bins.keys():
                count_bins[c] += 1
            else:
                count_bins[c] = 1
        print(count_bins)
        most = 0
        least = sys.maxsize
        for count in count_bins.values():
            if count > most:
                most = count
            if count < least:
                least = count
    else:
        # Find count for 20 iteration of every rule
        count_per_rule = {}
        for rule in pair_insertion_rules.keys():
            count_per_rule[rule] = count_after_x_steps(rule, 20, pair_insertion_rules)

        total_count_bin = {}
        # Count 40 steps for polymer template
        for n in range(0, len(polymer_template) - 1):
            count_bin = count_after_40_steps(polymer_template[n:n + 2], count_per_rule)
            sum_bins(total_count_bin, count_bin)
            print(total_count_bin)
        # Add last char
        total_count_bin[polymer_template[-1]] += 1

        print(total_count_bin)
        most = 0
        least = sys.maxsize
        for count in total_count_bin.values():
            if count > most:
                most = count
            if count < least:
                least = count

    print(f"Answer: {most} - {least} = {most - least}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
