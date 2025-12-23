#!/usr/bin/env python3
"""
AdventOfCode day 6.
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

    if args.second:
        result = 0
        time = int(lines[0].strip('\n').split(':')[1].replace(' ', ''))
        distance = int(lines[1].strip('\n').split(':')[1].replace(' ', ''))
        print(f"time: {time}, distance: {distance}")
        # Find by half search
        distance_target = distance + 1
        speed = time
        start_speed = 0
        while(distance_target > distance and speed > 1):
            speed = speed // 2
            # mm/ms
            distance_target = (time - speed) * speed
            print(f"speed: {speed}, distance: {distance_target}")
        for s in range(speed, speed * 2):
            distance_target = (time - s) * s
            if distance_target > distance:
                start_speed = s
                break
        print(f"start_speed: {start_speed}")

        distance_target = distance + 1
        stop_speed = 0
        speed_offs = time // 2
        speed = time // 2
        speed_head = time // 2
        speed_tail = time
        while(speed_offs > 1):
            speed_offs = (speed_tail - speed_head) // 2
            speed = speed_head + speed_offs
            # mm/ms
            distance_target = (time - speed) * speed
            if distance_target > distance:
                speed_head += (speed_tail - speed_head) // 2
            else:
                speed_tail -= (speed_tail - speed_head) // 2

            print(f"speed: {speed}, distance: {distance_target}, head/tail {speed_head}/{speed_tail}")

        stop_speed = speed_head
        print(f"stop_speed: {stop_speed}")

        result = stop_speed - start_speed + 1

    else:
        result = 1
        times_str = lines[0].strip('\n').split(':')[1].split(' ')
        dist_str = lines[1].strip('\n').split(':')[1].split(' ')
        
        races = []
        for str in times_str:
            if str:
                races.append({'time': int(str)})

        i = 0
        for str in dist_str:
            if str:
                races[i]['distance'] = int(str)
                i += 1

        for race in races:
            race['wins'] = 0
            for speed in range(1, race['time']):
                # mm/ms
                distance = (race['time'] - speed) * speed
                print(distance)
                if (distance > race['distance']):
                    race['wins'] += 1

        print(races)

        for race in races:
            result *= race['wins']

    print(f"result: {result}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
