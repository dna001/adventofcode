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


def check_safe(report):
    """Check if report is safe."""
    print(report)
    increasing = None
    safe = True
    for i in range(1, len(report)):
        diff = report[i - 1] - report[i]
        if diff > 0 and diff <= 3:
            if increasing == None:
                increasing = True
            elif not increasing:
                safe = False
                break
        elif diff < 0 and diff >= -3:
            if increasing == None:
                increasing = False
            elif increasing:
                safe = False
                break
        else:
            safe = False
            break
    return safe


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

    report_list = []
    for line in lines:
        line = line.strip('\n')
        numbers = line.split(' ')
        num_list = []
        for num in numbers:
            num_list.append(int(num))
        report_list.append(num_list)

    if args.second:
        safe_reports = 0
        for report in report_list:
            if check_safe(report):
                safe_reports += 1
            else:
                # Test to remove one number and see if report is still safe
                for i in range(0, len(report)):
                    new_report = report.copy()
                    del new_report[i]
                    if check_safe(new_report):
                        print("Found new safe report")
                        safe_reports += 1
                        break

        print(f'Safe reports: {safe_reports}')

    else:
        safe_reports = 0
        for report in report_list:
            if check_safe(report):
                safe_reports += 1

        print(f'Safe reports: {safe_reports}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
