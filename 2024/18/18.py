#!/usr/bin/env python3
"""
AdventOfCode day 18.
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
                #cost = self.calc_neighbour_cost(node['parent'], node['user_node'])
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
                    #neigbour_cost = self.calc_neighbour_cost(node, neighbour_node)

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


def print_map(map):
    """Print map."""
    for row in map:
        row_string = ""
        for col in row:
            row_string += col
        print(row_string)


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

    byte_coords = []
    for line in lines:
        line = line.strip('\n')
        values = line.split(',')
        coords = {'x': int(values[0]), 'y': int(values[1])}
        byte_coords.append(coords)

    print(byte_coords)

    if args.input.find('test') > 0:
        width = 7
        height = 7
        n = 12
    else:
        width = 71
        height = 71
        n = 1024

    # Generate map
    map = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append('.')
        map.append(row)
    #print_map(map)

    if args.second:
        found = False
        n_min = n
        n_max = len(byte_coords)
        path_found = True
        while not found:
            # Adjust n
            n = n_min + (n_max - n_min) // 2

            print(f"Testing n = {n} min: {n_min} min: {n_max}")
            # Generate map
            map = []
            for y in range(height):
                row = []
                for x in range(width):
                    row.append('.')
                map.append(row)

            # Add bytes to map
            for i in range(n):
                coord = byte_coords[i]
                map[coord['y']][coord['x']] = '#'

            print_map(map)
            # Convert to node list
            nodes = []
            # Add start node
            node = {'x': 0, 'y': 0, 'cost': 1}
            nodes.append(node)
            for y in range(len(map)):
                for x in range(len(map[0])):
                    if map[y][x] == '.':
                        node = {'x': x, 'y': y, 'cost': 1}
                        nodes.append(node)
            # Add end node
            node = {'x': len(map[0]) - 1, 'y': len(map) - 1, 'cost': 1}
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

            print(f"Cost: {cost}")
            
            if cost > 0:
                path_found = True
                n_min = n
            else:
                path_found = False
                n_max = n
            if n_max - n_min <= 1:
                break
        print(f"First exit prevention: {byte_coords[n_min]}")
    else:
        # Add bytes to map
        for i in range(n):
            coord = byte_coords[i]
            map[coord['y']][coord['x']] = '#'

        print_map(map)
        # Convert to node list
        nodes = []
        # Add start node
        node = {'x': 0, 'y': 0, 'cost': 1}
        nodes.append(node)
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y][x] == '.':
                    node = {'x': x, 'y': y, 'cost': 1}
                    nodes.append(node)
        # Add end node
        node = {'x': len(map[0]) - 1, 'y': len(map) - 1, 'cost': 1}
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

        print(f"Cost: {cost}")

    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
