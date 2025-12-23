#!/usr/bin/env python3
"""
AdventOfCode day 16.
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
    turn = 0
    fields = {}
    your_ticket = []
    nearby_tickets = []
    read_state = 'fields'

    # Read input
    try:
        with open(args.input, 'rt') as file:
            for line in file:
                line = line.strip('\n\r')
                if len(line) > 0 and 'nearby tickets' in line:
                    read_state = 'nearby_tickets'
                elif len(line) > 0 and 'your ticket' in line:
                    read_state = 'your_ticket'
                elif read_state == 'fields' and len(line) > 0:
                    field = line.split(':')[0]
                    range_1 = line.split(':')[1].split('o')[0]
                    range_2 = line.split(':')[1].split('r')[1]
                    fields[field] = [{'start': int(range_1.split('-')[0]), 'stop': int(range_1.split('-')[1])},
                                     {'start': int(range_2.split('-')[0]), 'stop': int(range_2.split('-')[1])}]
                elif read_state == 'your_ticket' and len(line) > 0:
                    field_vals = line.split(',')
                    for val in field_vals:
                        your_ticket.append(int(val))
                elif read_state == 'nearby_tickets' and len(line) > 0:
                    field_vals = line.split(',')
                    vals = []
                    for val in field_vals:
                        vals.append(int(val))
                    nearby_tickets.append(vals)

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(fields)
    #print(your_ticket)
    #print(nearby_tickets)

    start_time = datetime.now()

    summary_invalid_fields = 0
    valid_tickets = []

    count = 0
    for ticket in nearby_tickets:
        valid_ticket = True
        for num in ticket:
            found = False
            valid_ranges = 0
            for _, field in fields.items():
                for rng in field:
                    if num >= rng['start'] and num <= rng['stop']:
                        valid_ranges += 1
                        break
            if valid_ranges == 0:
                print("Bad field num {} for ticket {}".format(num, count))
                summary_invalid_fields += num
                valid_ticket = False

        if valid_ticket:
            valid_tickets.append(ticket)

        count += 1

    if not args.second:
        print("Ticket scanning error rate: {}".format(summary_invalid_fields))
    else:
        print(valid_tickets)
        field_matches = {}
        for field_name, ranges in fields.items():
            field_matches[field_name] = []
            for num in range(0, len(valid_tickets[0])):
                field_match = True
                for ticket in valid_tickets:
                    if ticket[num] >= ranges[0]['start'] and ticket[num] <= ranges[0]['stop'] or \
                        ticket[num] >= ranges[1]['start'] and ticket[num] <= ranges[1]['stop']:
                        field_match = True
                    else:
                        field_match = False
                        break
                if field_match:
                    print("Field: {} matches field number: {}".format(field_name, num))
                    field_matches[field_name].append(num)

        # Loop base on number of matches
        print(field_matches)
        found_nums = []
        found_fields = {}
        for num_matches in range(1, len(valid_tickets[0]) + 1):
            for field_name, matches in field_matches.items():
                if len(matches) == num_matches:
                    print("field {} len {}".format(field_name, num_matches))
                    for num in matches:
                        if num not in found_nums:
                            found_fields[field_name] = num
                            found_nums.append(num)

            print(found_nums)

        found_nums.sort()
        print(found_nums)
        print(found_fields)

        answer = 1
        count = 0
        for field_name, field_num in found_fields.items():
            if 'departure' in field_name:
                answer *= your_ticket[field_num]
                count += 1

        print(count)
        print("Answer: {}".format(answer))
        # 4702880 wrong

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
