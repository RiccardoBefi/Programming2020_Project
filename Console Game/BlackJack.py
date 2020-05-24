from Deck_creation import deck, listed, draw, game
import numpy as np


def check_input_b(players = 1, decks = 1, decision = 1):
    if inp < 1:
        raise ValueError("Number of players can't be lower than 1")
    if decks < 1:
        raise ValueError("Number of decks must be at least 1")

inp = int(input("What is the number of players you desire?\n"))
check_input_b(inp)

decks = int(input("What is the number of decks you desire to play with?\n"))
check_input_b(inp, decks)

game_deck = deck(decks)
player_i = game(inp + 2)
L = listed()

def winner(table, player_result):
    if table < 21:
        for i in range(1,inp+1):
            if player_result[i-1] > table and player_result[i-1] <= 21:
                print("Player", i, "has won.")
            else:
                print("The table has won.")
    else:
        print("The table went bust")
        for i in range(1,inp+1):
            if player_result[i-1] <= 21:
                print("Player", i, "has won.")


result = np.zeros(inp)
for p in range(1,inp+1):
    print("Player", p, "turn:\n")
    move = input("What is your decision?\n")
    check_input_b(inp, decks, move)
    while (move == "0"):
        draw_1, game_deck, player_i[p-1] = draw(game_deck, p)
        result[p-1] += int(L[draw_1, 0])
        if result[p-1] > 21:
            print("Player ",p, "has lost with a total value of", int(result[p-1]))
            break
        else:
            move = input("What is your decision?\n")
            check_input_b(inp, decks, move)

table_result = 0
while (table_result <= 16):
    draw_1, game_deck,player_i[inp] = draw(game_deck, inp)
    table_result += int(L[draw_1, 0])

winner(table_result, result)
