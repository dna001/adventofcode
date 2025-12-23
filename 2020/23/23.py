#!/usr/bin/env python3
"""
AdventOfCode day 23.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
from pprint import pprint
from enum import Enum


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

class NodeConstants(Enum):
    FRONT_NODE = 1


class Node:
    def __init__(self, element=None, next_node=None):
        self.element = element
        self.next_node = next_node

    def __str__(self):
        if self.element:
            return self.element.__str__()
        else:
            return 'Empty Node'


class CircularLinkedList:
    def __init__(self):
        self.head = Node(element=NodeConstants.FRONT_NODE)
        self.head.next_node = self.head
        self.max_value = 0
        self.min_value = 99

    def size(self):
        count = 0
        current = self.head.next_node
 
        while current != self.head:
            count += 1
            current = current.next_node
 
        return count        

    def add(self, data):
        node = self.head
        while node.next_node != self.head:
            node = node.next_node
        node.next_node = Node(data, self.head)
        if data > self.max_value:
            self.max_value = data
        if data < self.min_value:
            self.min_value = data

    def insert_after(self, node, data):
        old_node = node.next_node
        node.next_node = Node(data, old_node)
        return node.next_node

    def find_node(self, data):
        node = self.head.next_node
        while node != self.head:
            if node.element == data:
                return node
            node = node.next_node
        return None

    def remove_node(self, node):
        prev_node = node.next_node
        while prev_node.next_node != node:
            prev_node = prev_node.next_node

        prev_node.next_node = node.next_node
        node.next_node = None

    def find_first(self):
        return self.head.next_node

    def find_next(self, node):
        if node.next_node == self.head:
            return self.head.next_node
        else:
            return node.next_node

    def display(self):
        node = self.head.next_node
        string = ""
        while node != self.head:
            string += " {}".format(node.element)
            node = node.next_node

        print(string)


def play_game(cups, turns_max):
    """Play game."""
    turns = 0
    current_cup = cups.find_first()
    while turns < turns_max:
        print("Current cup: {}".format(current_cup.element))
        pickedup_cups = []
        # Pick 3 cups clockwise from current_cup
        for _ in range(0, 3):
            node = cups.find_next(current_cup)
            pickedup_cups.append(node.element)
            cups.remove_node(node)

        #print(pickedup_cups)
        destination = current_cup.element - 1
        if destination < cups.min_value:
            destination = cups.max_value
        found = False
        while not found:
            node = cups.find_node(destination)
            #print(node)
            if not node:
                destination -= 1
                if destination < cups.min_value:
                    destination = cups.max_value
            else:
                found = True
        # Add picked up cups after destination cup
        for cup in pickedup_cups:
            node = cups.insert_after(node, cup)

        cups.display()
        current_cup = cups.find_next(current_cup)
        turns += 1


def main():
    """Main program."""
    args = get_args()

    cups = CircularLinkedList()

    # Read input
    try:
        with open(args.input, 'rt') as file:
            for line in file:
                line = line.strip('\n\r')
                for char in line:
                    cups.add(int(char))

    except IOError:
        print("Failed reading file!")
        sys.exit()

    cups.display()

    # Play
    play_game(cups, 100)

    answer = ""
    node = cups.find_node(1)
    node = cups.find_next(node)
    while node.element != 1:
        answer += str(node.element)
        node = cups.find_next(node)

    print("Answer: {}".format(answer))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
