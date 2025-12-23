#!/usr/bin/env python3
"""
AdventOfCode day 15.
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
                    #print(f"Node: x={x}, y={y}, cost={node['cost']}")
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

    cavern = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            line = file.readline()
            while line:
                line = line.strip("\n\r")
                row = []
                for c in line:
                    row.append(int(c))
                cavern.append(row)
                line = file.readline()

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print(cavern)

    if not args.second:
        # Convert to node list
        nodes = []
        for y in range(len(cavern)):
            for x in range(len(cavern[0])):
                node = {'x': x, 'y': y, 'cost': cavern[y][x]}
                nodes.append(node)
        # Add adjacent nodes
        for node in nodes:
            node['adjacent'] = []
            for x in [node['x'] - 1, node['x'] + 1]:
                adjacent_node = find_node(nodes, x, node['y'])
                if adjacent_node:
                    node['adjacent'].append(adjacent_node)
            for y in [node['y'] - 1, node['y'] + 1]:
                adjacent_node = find_node(nodes, node['x'], y)
                if adjacent_node:
                    node['adjacent'].append(adjacent_node)
        # Find path using A star algorihtm
        pathfinder = Pathfinder()
        cost = pathfinder.find_path(nodes[0], nodes[-1])

        print(f"Answer: Lowest risk = {cost}")
    else:
        # Convert to node list and add 5x5 tiles
        nodes = []
        for y in range(len(cavern)):
            for x in range(len(cavern[0])):
                for y_tile in range(5):
                    for x_tile in range(5):
                        cost = cavern[y][x] + x_tile + y_tile
                        if cost > 9:
                            cost = ((cost - 1) % 9) + 1
                        node = {'x': x + x_tile * len(cavern[0]),
                                'y': y + y_tile * len(cavern),
                                'cost': cost}
                        nodes.append(node)
        # Add adjacent nodes
        for node in nodes:
            node['adjacent'] = []
            for x in [node['x'] - 1, node['x'] + 1]:
                adjacent_node = find_node(nodes, x, node['y'])
                if adjacent_node:
                    node['adjacent'].append(adjacent_node)
            for y in [node['y'] - 1, node['y'] + 1]:
                adjacent_node = find_node(nodes, node['x'], y)
                if adjacent_node:
                    node['adjacent'].append(adjacent_node)
        # Find path using A star algorihtm
        pathfinder = Pathfinder()
        cost = pathfinder.find_path(nodes[0], find_node(nodes, len(cavern[0]) * 5 - 1, len(cavern) * 5 - 1))

        print(f"Answer: Lowest risk = {cost}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
