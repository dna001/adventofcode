#!/usr/bin/env python3
"""
AdventOfCode day 7.
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


def parse_luggage_rule(line, rules):
    """Parse luggage rule."""

    bags = line.split(',')

    words = line.split(' ')
    top_bag_type = words[0] + '-' + words[1]
    if len(bags) == 1 and 'contain no' in bags[0]:
        rules[top_bag_type] = None
    else:
        rule = {}
        pos = bags[0].find('contain')
        bags[0] = bags[0][pos + len('contain'):]
        for bag in bags:
            words = bag.split(' ')
            number = int(words[1])
            bag_type = words[2] + '-' + words[3]
            rule[bag_type] = number
        rules[top_bag_type] = rule


def get_bags(rules, bags):
    """Find bags in rules."""
    found = {}
    for key, value in rules.items():
        if value:
            for bag in bags.keys():
                if bag in value.keys():
                    found[key] = 1

    # Remove found keys from rules
    for key in found.keys():
        del rules[key]

    return found


def count_bags_deep(rules, bags, depth = 0):
    """Count bags in bag."""
    count = 0
    print(bags)
    for bag, value in bags.items():
        if rules[bag]:
            count += count_bags_deep(rules, rules[bag], depth + 1) * value
            if depth != 0:
                count += value
        else:
            count += value

    print("Depth: {} Count: {}".format(depth, count))
    
    return count


def main():
    """Main program."""
    args = get_args()
    total_rules = 0
    rules = {}
    n_bags = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                parse_luggage_rule(line, rules)
                total_rules += 1
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    #print(rules)

    if not args.second:
        bags = {'shiny-gold': 1}
        while len(bags) > 0:
            bags = get_bags(rules, bags)
            print(bags)
            n_bags += len(bags)

        print("Number of bag colors that can contain shiny bags: {} ({})".format(n_bags, total_rules))
    else:
        bags = {'shiny-gold': 1}
        n_bags = count_bags_deep(rules, bags)

        print("Number of bags in shiny bags: {} ({})".format(n_bags, total_rules))
        

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
