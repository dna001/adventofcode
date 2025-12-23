#!/usr/bin/env python3
"""
AdventOfCode day 4.
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


def calc_unmarked_sum(table):
    """Summarize all unmarked numbers in table."""
    unmarked_sum = 0
    for row in table:
        for n in range(0, len(row[0])):
            if (row[1] & 1 << n) == 0:
                unmarked_sum += row[0][n]

    return unmarked_sum


def main():
    """Main program."""
    args = get_args()
    numbers = []
    tables = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            #Read bingo numbers
            bingo_numbers = line.strip('\n\r').split(',')
            for num in bingo_numbers:
                numbers.append(int(num))
            line = file.readline()
            #Read bingo tables
            table = []
            line = file.readline()
            while line:
                if len(line.strip('\n\r')) == 0:
                    tables.append(table)
                    # New table
                    table = []
                else:
                    table_row = line.strip('\n\r').split(' ')
                    row = []
                    for num in table_row:
                        if len(num) > 0:
                            row.append(int(num))
                    table.append([row, 0])
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    last_winner_found = None
    for number in numbers:
        tables_to_remove = []
        # Mark numbers in tables
        for table in tables:
            for row in table:
                col = 0
                for n in range(0, len(row[0])):
                    if number == row[0][n]:
                        row[1] |= 1 << n
                        for row_check in table:
                            if (row_check[1] & 1 << n) != 0:
                                col += 1
                if row[1] == 0x1f or col == 5:
                    if args.second:
                        print(f"Winner found, num: {number} row: {row[1]} col:{col}")
                        last_winner_found = (number, table)
                        tables_to_remove.append(table)
                        break
                    else:
                        # Winner found
                        # Calculate sum of unmarked numbers
                        board_unmarked_sum = calc_unmarked_sum(table)
                        print(table)
                        print(f"Unmarked sum {board_unmarked_sum}")
                        answer = board_unmarked_sum * number
                        print(f"Answer {board_unmarked_sum} * {number} = {answer}")
                        return 0

        # Check tables to remove
        for rm_table in tables_to_remove:
            #print(rm_table)
            tables.remove(rm_table)

    if last_winner_found:
        # Last winner found
        board_unmarked_sum = calc_unmarked_sum(last_winner_found[1])
        print(last_winner_found)
        print(f"Last table unmarked sum {board_unmarked_sum}")
        answer = board_unmarked_sum * last_winner_found[0]
        print(f"Answer {board_unmarked_sum} * {last_winner_found[0]} = {answer}")

    #answer = gamma_rate * epsilon_rate
        #print(f"Answer {gamma_rate} * {epsilon_rate} = {answer}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
