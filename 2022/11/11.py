#!/usr/bin/env python3
"""
AdventOfCode day 11.
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
    monkeys = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            id = 0
            line = file.readline().strip('\n')
            while 'Monkey' in line:
                # Read 5 lines
                monkey = {'id': id}
                # Read Starting items
                line = file.readline().strip('\n')
                items = line[line.find(':') + 1:].split(', ')
                #print(items)
                monkey['items'] = []
                for item in items:
                    monkey['items'].append(int(item))
                # Read Operation
                line = file.readline().strip('\n')
                operation = line[line.find('old') + 4:]
                #print(operation)
                if '*' in operation:
                    monkey['operation'] = '*'
                elif '+' in operation:
                    monkey['operation'] = '+'
                if 'old' in operation:
                    monkey['operation_val'] = 'old'
                else:
                    monkey['operation_val'] = int(operation[operation.find(' '):])
                # Read Test
                line = file.readline().strip('\n')
                div = int(line[line.find('by') + 3:])
                monkey['test_div'] = div
                # Read Test true
                line = file.readline().strip('\n')
                monkey['test_true_throw'] = int(line[-2:])
                # Read Test false
                line = file.readline().strip('\n')
                monkey['test_false_throw'] = int(line[-2:])
                monkey['inspections'] = 0
                id += 1
                # Skip empty line
                file.readline().strip('\n')
                line = file.readline().strip('\n')
                monkeys.append(monkey)

    except IOError:
        print("Failed reading file!")
        sys.exit()


    for round in range(0, 20):
        for monkey in monkeys:
            #print(monkey)
            while len(monkey['items']) > 0:
                item_val = monkey['items'].pop(0)
                if monkey['operation_val'] == 'old':
                    operation_val = item_val
                else:
                    operation_val = monkey['operation_val']
                if monkey['operation'] == '+':
                    item_val = item_val + operation_val
                elif monkey['operation'] == '*':
                    item_val = item_val * operation_val
                # Divide by 3
                item_val = math.floor(item_val / 3)
                # Throw to next monkey
                if item_val % monkey['test_div'] == 0:
                    monkeys[monkey['test_true_throw']]['items'].append(item_val)
                else:
                    monkeys[monkey['test_false_throw']]['items'].append(item_val)
                monkey['inspections'] += 1

    inspection_list = []
    for monkey in monkeys:
        print(monkey)
        inspection_list.append(monkey['inspections'])

    inspection_list.sort()
    monkey_business = inspection_list[-1] * inspection_list[-2]
    print(f"Level of monkey business: {monkey_business}")
    #if args.second:
    #else:
    #    print(f"Signal strength sum; {cpu_state['signal_strength_sum']}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
