# Functions to be tested

def check_input_b(players = 1, decks = 1, decision = 1):
    if players < 1:
        raise ValueError("Number of players can't be lower than 1")
    if decks < 1:
        raise ValueError("Number of decks must be at least 1")
    if decision not in [0,1]:
        raise ValueError("Command unknown, you must enter 0 or 1")