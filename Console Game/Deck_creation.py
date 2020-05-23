import numpy as np
import random as rn

# Deck creation
def deck(number_of_decks):
    rand_deck = []
    for i in range(1, number_of_decks+1):
        rand_deck = np.append(rand_deck, np.arange(0,52))
    rn.shuffle(rand_deck)
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

def game(keyboard):
    player_list = []
    for i in range(1,keyboard):
        globals()["player"+str(i)] = []
        player_list.append(globals()["player"+str(i)])
    return (player_list)

# Draw a card
def draw(d, active_player):
    first = int(d[0])
    rest = d[1:]
    seen = L[first, :]
    new_hand = np.hstack((active_player, first))
    print("The drawn card was:", seen)
    return(first, rest, new_hand)
