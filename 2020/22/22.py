#!/usr/bin/env python3
"""
AdventOfCode day 22.
"""

import argparse
import logging
import os
import sys
import json
import fnmatch
from datetime import datetime
from pprint import pprint


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

def check_previous_decks(prev_decks, deck1, deck2):
    """Check part of previous deck."""
    for decks in prev_decks:
        match = True
        if len(deck1) != len(decks['d1']) or len(deck2) != len(decks['d2']):
            continue
        for pos in range(0, len(deck1)):
            if deck1[pos] != decks['d1'][pos]:
                match = False
                break
        if match:
            for pos in range(0, len(deck2)):
                if deck2[pos] != decks['d2'][pos]:
                    match = False
                    break
        if match:
            #print("Player 1 deck: {}".format(deck1))
            #print("Player 2 deck: {}".format(deck2))
            return True

    return False


def play_game(deck1, deck2, sub_game, depth=0):
    """Play game or sub game."""
    turns = 0
    prev_decks = []
    prev_decks.append({'d1': deck1.copy(), 'd2': deck2.copy()})
    while len(deck1) > 0 and len(deck2) > 0:
        # Draw card
        card_p1 = deck1.pop(0)
        card_p2 = deck2.pop(0)
        if sub_game:
            if check_previous_decks(prev_decks, deck1, deck2):
                #print(prev_decks)
                #print("Detected!")
                return turns, 'p1'
            else:
                prev_decks.append({'d1': deck1.copy(), 'd2': deck2.copy()})

        if sub_game and card_p1 <= len(deck1) and card_p2 <= len(deck2):
            #print("Sub game! {}".format(depth + 1))
            deck1_new = deck1.copy()[0:card_p1]
            deck2_new = deck2.copy()[0:card_p2]
            game_turns, winner = play_game(deck1_new, deck2_new, sub_game, depth + 1)
            turns += game_turns
            if winner == 'p1':
                deck1.append(card_p1)
                deck1.append(card_p2)
            else:
                deck2.append(card_p2)
                deck2.append(card_p1)
        elif card_p1 > card_p2:
            deck1.append(card_p1)
            deck1.append(card_p2)
        else:
            deck2.append(card_p2)
            deck2.append(card_p1)

        #print("Player 1 deck: {}".format(deck1))
        #print("Player 2 deck: {}".format(deck2))
        #print("Turns: {}".format(turns))
        turns += 1

    if len(deck1) == 0:
        winner = 'p2'
    else:
        winner = 'p1'

    return turns, winner


def main():
    """Main program."""
    args = get_args()

    player1_deck = []
    player2_deck = []

    # Read input
    try:
        with open(args.input, 'rt') as file:
            player = 1
            for line in file:
                line = line.strip('\n\r')
                if "Player 1" in line:
                    deck = player1_deck
                elif "Player 2" in line:
                    deck = player2_deck
                elif len(line) > 0:
                    deck.append(int(line))

    except IOError:
        print("Failed reading file!")
        sys.exit()

    print("Player 1 deck: {}".format(player1_deck))
    print("Player 2 deck: {}".format(player2_deck))

    # Play
    turns, winner = play_game(player1_deck, player2_deck, args.second)

    score = 0
    if winner == 'p1':
        deck = player1_deck
        winner = "Player 1"
        print("Player 1 deck: {}".format(player1_deck))
    else:
        deck = player2_deck
        winner = "Player 2"
        print("Player 2 deck: {}".format(player2_deck))

    multiplier = 1
    for pos in range(0, len(deck)):
        score += deck[-(pos + 1)] * multiplier
        multiplier += 1

    print("Winner: {} Score: {} Turns: {}".format(winner, score, turns))
    #input("Press any key to continue...")


if __name__ == "__main__":
    main()
