#!/usr/bin/env python3
"""
AdventOfCode day 8.
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


def sort_by_dist(r):
    """ Sort by distance. """
    return r['dist']


def sort_by_array_size(r):
    """ Sort by array size. """
    return len(r)


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

    coords = []
    for line in lines:
        tmp = line.strip('\n')
        coord = []
        coord_tuple = tmp.split(',')
        coord.append(int(coord_tuple[0]))
        coord.append(int(coord_tuple[1]))
        coord.append(int(coord_tuple[2]))
        coords.append(coord)

    print(coords)

    dist_list = []
    for i in range(len(coords)):
        c = coords[i]
        for j in range(i + 1, len(coords)):
            c2 = coords[j]
            dist = (c2[0] - c[0])**2 + (c2[1] - c[1])**2 + (c2[2] - c[2])**2
            dist_list.append({'a': i, 'b': j, 'dist': dist})
    
    dist_list.sort(key=sort_by_dist)
    print(dist_list[:10])

    if args.second:
        answer = 0
        circuits = []
        i = 0
        for dist in dist_list:
            c1 = []
            c2 = []
            for c in circuits:
                if dist['a'] in c:
                    c1 = c
                if dist['b'] in c:
                    c2 = c

            if len(c1) > 0 and len(c2) > 0:
                # merge lists:
                if c1 != c2:
                    circuits.remove(c1)
                    c2.extend(c1)
            elif len(c1) > 0:
                if dist['b'] not in c1:
                    c1.append(dist['b'])
            elif len(c2) > 0:
                if dist['a'] not in c2:
                    c2.append(dist['a'])
            else:
                circuits.append([dist['a'], dist['b']])
            
            print(circuits)
            i += 1
            if (len(circuits[0]) == len(coords)):
                print(dist)
                answer = dist
                break

        print(f'Answer {coords[answer['a']][0] * coords[answer['b']][0]}')
    else:
        circuits = []
        if 'test' in args.input:
            max_i = 10
        else:
            max_i = 1000
        i = 0
        for dist in dist_list:
            c1 = []
            c2 = []
            for c in circuits:
                if dist['a'] in c:
                    c1 = c
                if dist['b'] in c:
                    c2 = c

            if len(c1) > 0 and len(c2) > 0:
                # merge lists:
                if c1 != c2:
                    circuits.remove(c1)
                    c2.extend(c1)
            elif len(c1) > 0:
                if dist['b'] not in c1:
                    c1.append(dist['b'])
            elif len(c2) > 0:
                if dist['a'] not in c2:
                    c2.append(dist['a'])
            else:
                circuits.append([dist['a'], dist['b']])
            
            print(circuits)
            i += 1
            if i == max_i:
                break

        circuits.sort(key=sort_by_array_size)
        circuits.reverse()
        print(circuits)

        # Multiply sizes of the 3 largest circuits
        answer = len(circuits[0]) * len(circuits[1]) * len(circuits[2])
        print(f'Answer {answer}')

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
