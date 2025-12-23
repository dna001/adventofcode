#!/usr/bin/env python3
"""
AdventOfCode day 2.
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
    cal_value_sum = 0

    # Read input
    try:
        with open(args.input, 'rt') as file:
            lines = file.readlines()
    except IOError:
        print("Failed reading file!")
        sys.exit()

    red_max_count = 12
    green_max_count = 13
    blue_max_count = 14
    result = 0
    if args.second:
        for line in lines:
            line = line.strip('\n')
            game_id, games = line.split(':')
            game_id = int(game_id[4:])
            game_rounds = games.split(';')
            min_red_count = 0
            min_green_count = 0
            min_blue_count = 0
            for round in game_rounds:
                colors = round.split(',')
                for color_line in colors:
                    value = int(color_line.split(' ')[1])
                    color = color_line.split(' ')[2]
                    print(f"v:{value}, c:{color}")
                    if "red" in color_line and value > min_red_count:
                        min_red_count = value
                    elif "green" in color_line and value > min_green_count:
                        min_green_count = value
                    elif "blue" in color_line and value > min_blue_count:
                        min_blue_count = value
            power = min_red_count * min_green_count * min_blue_count
            print(f"r/g/b:{min_red_count}{min_green_count}{min_blue_count}, power:{power}")
            result += power
    else:
        for line in lines:
            line = line.strip('\n')
            game_id, games = line.split(':')
            game_id = int(game_id[4:])
            game_rounds = games.split(';')
            valid = True
            for round in game_rounds:
                print(round)
                colors = round.split(',')
                for color_line in colors:
                    value = int(color_line.split(' ')[1])
                    color = color_line.split(' ')[2]
                    print(f"v:{value}, c:{color}")
                    if "red" in color_line and value > red_max_count:
                        valid = False
                        break
                    elif "green" in color_line and value > green_max_count:
                        valid = False
                        break
                    elif "blue" in color_line and value > blue_max_count:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                print(f"id: {game_id} is valid")
                result += game_id

    print(f"result: {result}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
