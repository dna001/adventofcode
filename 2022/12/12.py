#!/usr/bin/env python3
"""
AdventOfCode day 12.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
import math
import copy

sum_of_total_sizes = 0

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


class Pathfinder:
    """The A - star pathfinder implementation.
        Pseudo - code A star

        create the open list of nodes, initially containing only our starting node
        create the closed list of nodes, initially empty
        while (we have not reached our goal) {
            consider the best node in the open list (the node with the lowest f value)
            if (this node is the goal) {
                then we're done
            }
            else {
                move the current node to the closed list and consider all of its neighbors
                for (each neighbor) {
                    if (this neighbor is in the closed list and our current g value is lower) {
                        update the neighbor with the new, lower, g value
                        change the neighbor's parent to our current node
                    }
                    else if (this neighbor is in the open list and our current g value is lower) {
                        update the neighbor with the new, lower, g value
                        change the neighbor's parent to our current node
                    }
                    else this neighbor is not in either the open or closed list {
                        add the neighbor to the open list and set its g value
                    }
                }
            }
        }
    """

    def __init__(self):
        self.path = []
        self.open_list = []
        self.closed_list = []

    def create_node(self, user_node, h):
        """ Create new node. """
        node = {'user_node': user_node,
                'g': 0,  # The exact cost from the starting node
                'h': h,  # Estimated (heuristic cost) to destination
                'f': h,  # Total cost to destination (f=g+h)
                'cost': user_node['cost'],  # Cost for this node
                'parent': None
                }
        return node

    def calculate_h(self, start, end):
        """ Calculate H using manhattan distance. """
        return abs(end['x'] - start['x']) + abs(end['y'] - start['y'])

    def node_pop(self, node_list):
        """ Pop node with lowest f value from list. """
        if len(node_list) > 0:
            best_node = node_list[0]
        else:
            return None

        for node in node_list:
            if node['f'] < best_node['f']:
                best_node = node

        node_list.remove(best_node)
        return best_node

    def find_node(self, node_list, user_node):
        """ Find user node in node list. """
        for node in node_list:
            if node['user_node'] == user_node:
                return node

        return None

    def find_path(self, start, end):
        """ Find path and return cost. """
        new_node = self.create_node(start, self.calculate_h(start, end))
        self.open_list.append(new_node)

        node = self.node_pop(self.open_list)
        while node:
            # Consider the best node in the open list (the node with the lowest f value)
            if node['user_node'] == end:
                # Path found
                #n = node_count(node);
                #print(f"Nodes = {n}")
                cost = 0
                # Calculate cost (skip start node)
                while node['parent']:
                    x = node['user_node']['x']
                    y = node['user_node']['y']
                    print(f"Node: x={x}, y={y}, cost={node['cost']} g={node['g']} val={node['user_node']['val']}")
                    cost += node['cost']
                    node = node['parent']
                return cost
            else:
                # Move current node to closed list
                self.closed_list.append(node)
                # Find neighbours
                for neighbour_node in node['user_node']['adjacent']:
                    open_node = self.find_node(self.open_list, neighbour_node)
                    closed_node = self.find_node(self.closed_list, neighbour_node)

                    if closed_node and closed_node['g'] > node['g'] + neighbour_node['cost']:
                        # Update the neighbor with the new, lower, g value
                        closed_node['g'] = node['g'] + neighbour_node['cost']
                        # Change the neighbor's parent to our current node
                        closed_node['parent'] = node
                    elif open_node and open_node['g'] > node['g'] + neighbour_node['cost']:
                        # Update the neighbor with the new, lower, g value
                        open_node['g'] = node['g'] + neighbour_node['cost']
                        # Change the neighbor's parent to our current node
                        open_node['parent'] = node
                    elif not open_node and not closed_node:
                        # This neighbor is not in either the open or closed list
                        # Add the neighbor to the open list and set its g value.
                        new_node = self.create_node(neighbour_node, self.calculate_h(neighbour_node, end))
                        new_node['g'] = node['g'] + neighbour_node['cost']
                        new_node['f'] = new_node['g'] + new_node['h']
                        new_node['parent'] = node
                        #print(f"New node: cost={new_node['cost']} g={new_node['g']} h={new_node['h']} f={new_node['f']}")
                        self.open_list.append(new_node)

                node = self.node_pop(self.open_list)
        return 0


def find_node(nodes, x, y):
    """ Find node based on coordinates. """
    for node in nodes:
        if node['x'] == x and node['y'] == y:
            return node

    return None


def main():
    """Main program."""
    args = get_args()
    heightmap = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline().strip('\n')
            while line:
                heightmap.append(line)
                line = file.readline().strip('\n')

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(heightmap)

    # Convert to node list
    nodes = []
    for y in range(len(heightmap)):
        for x in range(len(heightmap[0])):
            node = {'x': x, 'y': y, 'cost': 1, 'val': heightmap[y][x]}
            if heightmap[y][x] == 'S':
                node['val'] = 'a'
                start_node = node
            elif heightmap[y][x] == 'E':
                node['val'] = 'z'
                end_node = node
            nodes.append(node)
    # Add valid adjacent nodes
    for node in nodes:
        node['adjacent'] = []
        for x in [node['x'] - 1, node['x'] + 1]:
            adjacent_node = find_node(nodes, x, node['y'])
            if adjacent_node:
                if ord(adjacent_node['val']) <= ord(node['val']) or ord(node['val']) + 1 == ord(adjacent_node['val']):
                    node['adjacent'].append(adjacent_node)
        for y in [node['y'] - 1, node['y'] + 1]:
            adjacent_node = find_node(nodes, node['x'], y)
            if adjacent_node:
                if ord(adjacent_node['val']) <= ord(node['val']) or ord(node['val']) + 1 == ord(adjacent_node['val']):
                    node['adjacent'].append(adjacent_node)
    # Find path using A star algorihtm
    pathfinder = Pathfinder()
    cost = pathfinder.find_path(start_node, end_node)

    print(f"Cost: {cost}")

    #if args.second:
        #for row in range(0, 6):
        #    print(f"{cpu_state['pixel_matrix'][row * 40: row * 40 + 40]}")
    #else:
        #print(f"Signal strength sum; {cpu_state['signal_strength_sum']}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
