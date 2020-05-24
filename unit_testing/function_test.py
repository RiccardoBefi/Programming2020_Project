# Functions to be tested

import numpy as np


def check_input_blackjack(players = 1, decks = 1):
    if players < 1:
        raise ValueError("Number of players can't be lower than 1")
    if decks < 1:
        raise ValueError("Number of decks must be at least 1")
        
def deck(number_of_decks = 1):
    rand_deck = []
    for i in range(1, number_of_decks + 1):
        rand_deck = np.append(rand_deck, np.arange(0,52))
    #rn.shuffle(rand_deck)
    return(rand_deck)
    
def listed():
    out = np.array(["nan", "nan"])
    sign = ["Hearts", "Diamonds", "Clubs", "Spades"]
    for s in range(0,4):
        for n in range(1,14):
            temp = [n, sign[s]]
            out = np.vstack((out,temp))
    out = out[1:53]
    return (out)

L = listed()

def draw(d = deck(), active_player = 1):
    first = int(d[0])
    rest = d[1:]
    seen = L[first, :]
    new_hand = np.hstack((active_player, first))
    #print("The drawn card was:", seen)
    return(first, rest, new_hand)
