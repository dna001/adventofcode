#!/usr/bin/env python3
"""
AdventOfCode day 5.
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


def find_rules_for_page_after(page, rules):
    """Find and return list of pages that should be after page."""
    page_list = []
    for rule in rules:
        if rule['page'] == page:
            page_list.append(rule['after'])
    return page_list


def find_rules_for_page_before(page, rules):
    """Find and return list of pages that should be before page."""
    page_list = []
    for rule in rules:
        if rule['after'] == page:
            page_list.append(rule['page'])
    return page_list


def find_and_remove_page(page, list):
    """Remove page from list if found."""
    page_found = False
    for p in list:
        if p == page:
            page_found = True
            break
    if page_found:
        list.remove(page)


def check_pages(pages, rules):
    """Check page ordering according to rules."""
    valid = True
    # Check first page
    for i in range(0, len(pages)):
        #print(f"page: {pages[i]}")
        page_list_before_ = find_rules_for_page_before(pages[i], rules)
        # remove pages not in list
        page_list_before = []
        for page in page_list_before_:
            if page in pages:
                page_list_before.append(page)
        #print(page_list_before)
        if len(page_list_before) > i:
            valid = False
            break
        for before in range(0, i):
            find_and_remove_page(pages[before], page_list_before)
        if len(page_list_before) != 0:
            valid = False
            break
        page_list_after_ = find_rules_for_page_after(pages[i], rules)
        # remove pages not in list
        page_list_after = []
        for page in page_list_after_:
            if page in pages:
                page_list_after.append(page)
        #print(page_list_after)
        if len(page_list_after) >= len(pages) - i:
            valid = False
            break
        for after in range(i + 1, len(pages)):
            find_and_remove_page(pages[after], page_list_after)
        #print(page_list_after)
        if len(page_list_after) != 0:
            valid = False
            break
    print(f"pages valid: {valid}")
    return valid


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

    page_ordering_rules_phase = True
    page_ordering_rules = []
    page_updates = []
    for line in lines:
        line = line.strip('\n')
        if len(line) > 0 and page_ordering_rules_phase:
            numbers = line.split('|')
            page_ordering_rules.append({'page': int(numbers[0]), 'after': int(numbers[1])})
        elif len(line) > 0 and not page_ordering_rules_phase:
            pages = line.split(',')
            pages_list = []
            for page in pages:
                pages_list.append(int(page))
            page_updates.append(pages_list)
        else:
            page_ordering_rules_phase = False

    print(page_ordering_rules)
    print(page_updates)

    if args.second:
        invalid_updates = []
        for page_update in page_updates:
            valid = check_pages(page_update, page_ordering_rules)
            if not valid:
                print(page_update)
                invalid_updates.append(page_update)
        print("----------------------------")
        corrected_order_update_middle_sum = 0
        # Order correct
        for update in invalid_updates:
            print(update)
            # Filter rules with only pages occuring in update
            filtered_rules = []
            for rule in page_ordering_rules:
                if rule['page'] in update and rule['after'] in update:
                    filtered_rules.append(rule)

            after_rules_for_page = [0 for i in range(len(update))]
            for page in update:
                print(f"page: {page}")
                rules_after = find_rules_for_page_before(page, filtered_rules)
                n_rules = len(rules_after)
                print("rules_after:")
                print(rules_after)
                after_rules_for_page[n_rules] = page
            corrected_order_update_middle_sum += after_rules_for_page[len(update) //2]

            print(f"Corrected order: {after_rules_for_page}")

        print(f"Sum middle page numbers of corrected ordered updates: {corrected_order_update_middle_sum}")

    else:
        correct_order_update_middle_sum = 0
        for page_update in page_updates:
            valid = check_pages(page_update, page_ordering_rules)
            if valid:
                print(page_update)
                print(f"middle: {len(page_update) // 2}")
                correct_order_update_middle_sum += page_update[len(page_update) // 2]

        print(f"Sum middle page numbers of ordered updates: {correct_order_update_middle_sum}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
