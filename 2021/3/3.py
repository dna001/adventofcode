#!/usr/bin/env python3
"""
AdventOfCode day 3.
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

def find_numbers(numbers, bit_pos, most_common):
    """Find most common value bits or least common value bits and return list."""
    new_numbers = []
    ones = 0
    zeroes = 0
    for number in numbers:
        for n in range(bit_pos, len(number)):
            if number[bit_pos] == '1':
                ones += 1
            else:
                zeroes += 1
    print(f"ones {ones}, zeroes {zeroes}")
    # Determine value to keep
    if most_common:
        if ones >= zeroes:
            value_to_keep = '1'
        else:
            value_to_keep = '0'
    else:
        if ones < zeroes:
            value_to_keep = '1'
        else:
            value_to_keep = '0'

    for number in numbers:
        if number[bit_pos] == value_to_keep:
            new_numbers.append(number)

    return new_numbers


def bin_to_int(number):
    """Convert binary string to int."""
    value = 0
    for n in range(0, len(number)):
        value *= 2
        if number[n] == '1':
            value += 1

    return value


def main():
    """Main program."""
    args = get_args()
    numbers = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                numbers.append(line.strip('\n\r'))
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    if not args.second:
        bin = [0] * len(numbers[0])
        for number in numbers:
            print(f"Number {number}")
            for n in range(0, len(number)):
                if number[n] == '1':
                    bin[n] += 1
                else:
                    bin[n] -= 1

        gamma_rate = 0
        epsilon_rate = 0
        for n in range(0, len(bin)):
            gamma_rate *= 2
            epsilon_rate *= 2
            if bin[n] > 0:
                gamma_rate += 1
            else:
                epsilon_rate += 1

        print(f"gamma rate {gamma_rate}, epsilon rate {epsilon_rate}")
        answer = gamma_rate * epsilon_rate
        print(f"Answer {gamma_rate} * {epsilon_rate} = {answer}")

    else:
        #Find oxygen generator rating (most common)
        new_numbers = numbers.copy()
        for n in range(0, len(numbers[0])):
            new_numbers = find_numbers(new_numbers, n, True)
            if len(new_numbers) == 1:
                break
        oxygen_generator_rating = bin_to_int(new_numbers[0])
        print(f"Oxygen generator rating {new_numbers[0]}, {oxygen_generator_rating}")

        #Find CO2 scrubber rating (most common)
        new_numbers = numbers.copy()
        for n in range(0, len(numbers[0])):
            new_numbers = find_numbers(new_numbers, n, False)
            if len(new_numbers) == 1:
                break
        co2_scrubber_rating = bin_to_int(new_numbers[0])
        print(f"CO2 scrubber rating {new_numbers[0]}, {co2_scrubber_rating}")

        answer = oxygen_generator_rating * co2_scrubber_rating
        print(f"Answer {oxygen_generator_rating} * {co2_scrubber_rating} = {answer}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
