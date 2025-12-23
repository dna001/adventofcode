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

    def calc_neighbour_cost(self, node, new_node):
        """Calculate real neighbour cost."""
        start_dir = 'E'
        cost = 1
        x_next = new_node['x']
        y_next = new_node['y']
        new_dir = 'X'
        old_dir = 'X'
        # Calculate cost from start
        while node['parent']:
            x = node['user_node']['x']
            y = node['user_node']['y']
            node_cost = node['cost']
            if x_next > x:
                new_dir = 'E'
            elif x_next < x:
                new_dir = 'W'
            elif y_next < y:
                new_dir = 'N'
            elif y_next > y:
                new_dir = 'S'
            #print(f"{new_dir}")
            if new_dir != old_dir and old_dir != 'X':
                node_cost += 1000
            old_dir = new_dir
            cost += node_cost
            #print(f"Node: x={x}, y={y}, cost={node_cost}")
            x_next = x
            y_next = y
            node = node['parent']
        if new_dir != 'E':
            print(f"Last dir: {new_dir}, add 90 cost")
            cost += 1000
        return cost


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
                #cost = 0
                # Calculate cost (skip start node)
                cost = self.calc_neighbour_cost(node['parent'], node['user_node'])
                #while node['parent']:
                #    x = node['user_node']['x']
                #    y = node['user_node']['y']
                    #print(f"Node: x={x}, y={y}, cost={node['cost']}")
                #    cost += node['cost']
                #    node = node['parent']
                return cost
            else:
                # Move current node to closed list
                self.closed_list.append(node)
                # Find neighbours
                for neighbour_node in node['user_node']['adjacent']:
                    open_node = self.find_node(self.open_list, neighbour_node)
                    closed_node = self.find_node(self.closed_list, neighbour_node)
                    neigbour_cost = self.calc_neighbour_cost(node, neighbour_node)

                    if closed_node and closed_node['g'] > neigbour_cost: # node['g'] + neighbour_node['cost']:
                        # Update the neighbor with the new, lower, g value
                        closed_node['g'] = neigbour_cost # node['g'] + neighbour_node['cost']
                        # Change the neighbor's parent to our current node
                        closed_node['parent'] = node
                    elif open_node and open_node['g'] > neigbour_cost: # node['g'] + neighbour_node['cost']:
                        # Update the neighbor with the new, lower, g value
                        open_node['g'] = neigbour_cost #node['g'] + neighbour_node['cost']
                        # Change the neighbor's parent to our current node
                        open_node['parent'] = node
                    elif not open_node and not closed_node:
                        # This neighbor is not in either the open or closed list
                        # Add the neighbor to the open list and set its g value.
                        new_node = self.create_node(neighbour_node, self.calculate_h(neighbour_node, end))
                        new_node['g'] = neigbour_cost # node['g'] + neighbour_node['cost']
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


def move_boxes(map, boxes, x_dir, y_dir):
    """Move all boxes one step in dir."""
    #print(boxes)
    boxes.reverse()
    #print(boxes)
    for box in boxes:
        map[box['y'] + y_dir][box['x'] + x_dir] = 'O'

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

    map = []
    for line in lines:
        line = line.strip('\n')
        row = []
        for char in line:
            row.append(char)
        map.append(row)

    print_map(map)

    if args.second:
        print(f"")
    else:
        # Convert to node list
        nodes = []
        # Add start node
        node = {'x': 1, 'y': len(map) - 2, 'cost': 1}
        nodes.append(node)
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y][x] == '.':
                    node = {'x': x, 'y': y, 'cost': 1}
                    nodes.append(node)
        # Add end node
        node = {'x': len(map[0]) -2, 'y': 1, 'cost': 1}
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
