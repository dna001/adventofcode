#!/usr/bin/env python3
"""
AdventOfCode day 10.
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


def sort_by_area(r):
    """ Sort by area. """
    return r['area']


def print_tiles(tiles):
    """ Print tiles. """
    if len(tiles) > 20:
        print("grid")
        return
    print("-----")
    for row in tiles:
        row_str = ""
        for tile in row:
            for i in range(32):
                if tile & (1 << (31 - i)):
                    row_str += '#'
                else:
                    row_str += '.'
        print(row_str)


def toggle_lights(lights, button):
    """ Toggle lights. """
    for l in button:
        if lights[l] == '.':
            lights[l] = '#'
        else:
            lights[l] = '.'


def light_compare(l1, l2):
    """ Compare lights. """
    match = True
    for i, l in enumerate(l1):
        if l2[i] != l:
            match = False
            break
    return match


def check_buttons(machine, light, depth, button_list):
    """ Toggle and check buttons recursively. """
    for b in machine['buttons']:
        l = light.copy()
        toggle_lights(l, b)
        #print(f'{l}, d: {depth}')
        if depth > 0:
            if check_buttons(machine, l, depth - 1, button_list):
                button_list.append(b)
                return True
        else:
            #print(f'{l} -- {machine['lights']}')
            if light_compare(l, machine['lights']):
                print('match')
                button_list.append(b)
                return True
        

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

    machines = []
    for line in lines:
        tmp = line.strip('\n')
        tmp = tmp.split(' ')
        lights = []
        for c in tmp[0][1:-1]:
            lights.append(c)
        buttons = []
        joltages = []
        for i in range(1, len(tmp)):
            if tmp[i][0] == '(':
                button_tmp = tmp[i][1:-1].split(',')
                button_lights = []
                for b in button_tmp:
                    button_lights.append(int(b))
                buttons.append(button_lights)
            else:
                joltage_tmp = tmp[i][1:-1].split(',')
                for j in joltage_tmp:
                    joltages.append(int(j))

        machine = {'lights': lights, 'buttons': buttons, 'joltages': joltages}
        machines.append(machine)

    print(machines)

    if args.second:
        answer = 0
        print(f'Answer {answer}')
    else:
        answer = 0
        num_buttons = []
        for machine in machines:
            print(f'Machine {machine['lights']}')
            found = False

            button_list = []
            for i in range(0, 10):
                l = ['.'] * len(machine['lights'])
                found = check_buttons(machine, l, i, button_list)
                if found:
                    print(f'Button list: {button_list}')
                    num_buttons.append(i + 1)
                    break

            # Try 3 buttons
            #for b1 in machine['buttons']:
            #    lights_base = ['.'] * len(machine['lights'])
            #    toggle_lights(lights_base, b1)
            #    for b2 in machine['buttons']:
            #        l2 = lights_base.copy()
            #        toggle_lights(l2, b2)
            #        for b3 in machine['buttons']:
            #            l3 = l2.copy()
            #            toggle_lights(l3, b3)
            #            if light_compare(l3, machine['lights']):
            #                print(f'b1: {b1}, b2: {b2}, b3: {b3}')
            #                found = True
            #                break
            #        if found:
            #            break
            #    if found:
            #        break
            #if found:
            #    num_buttons.append(3)
            #    continue

            if not found:
                print('Not found')

        print(num_buttons)
        for b in num_buttons:
            answer += b
        print(f'Answer {answer}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
