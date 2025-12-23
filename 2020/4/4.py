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


def validate_passport(line):
    """Validate passport."""
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    #print(line + '\n')
    for field in required_fields:
        if field not in line:
            print("Invalid passport: {}".format(line))
            return False

    return True

def validate_passport_2(line):
    """Validate passport."""
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    valid = True

    #print(line + '\n')
    for field in required_fields:
        if field not in line:
            print("Invalid passport. Field {} missing.\n{}".format(field, line))
            return False
        else:
            pos = line.find(field)
            field_text = line[pos + 4:].split(' ')[0]
            #print(field_text)
            if field == 'byr':
                if len(field_text) != 4 or int(field_text) < 1920 or int(field_text) > 2002:
                    valid = False
                    print("{}, {}".format(len(field_text), int(field_text)))
                    break
            if field == 'iyr':
                if len(field_text) != 4 or int(field_text) < 2010 or int(field_text) > 2020:
                    valid = False
                    break
            if field == 'eyr':
                if len(field_text) != 4 or int(field_text) < 2020 or int(field_text) > 2030:
                    valid = False
                    break
            if field == 'hgt':
                try:
                    value = int(field_text[:-2])
                except ValueError:
                    valid = False
                    break
                if 'cm' in field_text:
                    if value < 150 or value > 193:
                        valid = False
                        break
                elif 'in' in field_text:
                    if value < 59 or value > 76:
                        valid = False
                        break
                else:
                    valid = False
                    break;
            if field == 'hcl':
                valid_numbers = "0123456789abcdef"
                if '#' not in field_text or len(field_text) != 7:
                    valid = False
                    break
                for pos in range(1, len(field_text)):
                    if field_text[pos] not in valid_numbers:
                        valid = False
                        break
                if not valid:
                    break
            if field == 'ecl':
                valid_ecls = ['amb','blu','brn','gry','grn','hzl','oth']
                if len(field_text) != 3 or field_text not in valid_ecls:
                    valid = False
                    break
            if field == 'pid':
                valid_numbers = "0123456789"
                if len(field_text) != 9:
                    valid = False
                    break
                for pos in range(0, len(field_text)):
                    if field_text[pos] not in valid_numbers:
                        valid = False
                        break
                if not valid:
                    break

    if not valid:
        print("Invalid field {} ({}).\n{}".format(field, field_text, line))

    return valid

def main():
    """Main program."""
    args = get_args()
    lines = []
    total_passports = 0
    valid_passports = 0
    passport_text = ""

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip('\n\r')
                if len(line) > 0:
                    passport_text += line.strip('\n\r') + ' '
                else:
                    if not args.second:
                        if validate_passport(passport_text):
                            valid_passports += 1
                    else:
                        if validate_passport_2(passport_text):
                            valid_passports += 1
                    total_passports += 1
                    passport_text = ""
                line = file.readline()
            if not args.second:
                if validate_passport(passport_text):
                    valid_passports += 1
            else:
                if validate_passport_2(passport_text):
                    valid_passports += 1
            total_passports += 1

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print("Valid passports: {}/{}".format(valid_passports, total_passports))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
