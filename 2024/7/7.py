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

    equations = []
    for line in lines:
        line = line.strip('\n')
        parts = line.split(':')
        equation_item = {}
        equation_item['result'] = int(parts[0])
        values_string_list = parts[1].split(' ')
        values = []
        for value  in values_string_list:
            if len(value) > 0:
                values.append(int(value))
        equation_item['values'] = values
        equations.append(equation_item)

    print(equations)


    if args.second:
        # Generation operator test list
        operator_lists = []
        # 1
        operator_list = [['*'], ['+'], ['|']]
        operator_lists.append(operator_list)

        for i in range(10):
            operator_list = []
            for j in range(len(operator_lists[i])):
                operator_list.append(['*'] + operator_lists[i][j])
                operator_list.append(['+'] + operator_lists[i][j])
                operator_list.append(['|'] + operator_lists[i][j])
            operator_lists.append(operator_list)

        for operators in operator_lists:
            print(len(operators))

        found_equations = 0
        sum_equations = 0
        # Test operatiors + and * for solution
        for equation in equations:
            print(equation)
            found = False
            values = equation['values']
            for operators in operator_lists[len(values) - 2]:
                # print(operators)
                result = values[0]
                for i in range(len(operators)):
                    if operators[i] == '+':
                        result += values[i + 1]
                    elif operators[i] == '*':
                        result *= values[i + 1]
                    else:
                        old_result = result
                        result = int(str(result) + str(values[i + 1]))
                        # print(f"{old_result} || {values[i + 1]} = {result}")
                if result == equation['result']:
                    print("Found")
                    print(operators)
                    found = True
                    break
            if found:
                print(f"Found solution")
                found_equations += 1
                sum_equations += equation['result']

        print(f"Equations with solutions: {found_equations}, sum: {sum_equations}")

    else:
        # Generation operator test list
        operator_lists = []
        # 1
        operator_list = [['*'], ['+']]
        operator_lists.append(operator_list)

        for i in range(10):
            operator_list = []
            for j in range(len(operator_lists[i])):
                operator_list.append(['*'] + operator_lists[i][j])
                operator_list.append(['+'] + operator_lists[i][j])
            operator_lists.append(operator_list)

        print(operator_lists)
        found_equations = 0
        sum_equations = 0
        # Test operatiors + and * for solution
        for equation in equations:
            print(equation)
            found = False
            values = equation['values']
            for operators in operator_lists[len(values) - 2]:
                # print(operators)
                result = values[0]
                for i in range(len(operators)):
                    if operators[i] == '+':
                        result += values[i + 1]
                    else:
                        result *= values[i + 1]
                if result == equation['result']:
                    print("Found")
                    print(operators)
                    found = True
                    break
            if found:
                print(f"Found solution")
                found_equations += 1
                sum_equations += equation['result']

        print(f"Equations with solutions: {found_equations}, sum: {sum_equations}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
