from Deck_creation import draw, listed, deck, game

l = listed()
game_deck = deck(1)

total_players = game(3)

player_1_hand = total_players[0]; player_2_hand = total_players[1]

# Turn base
stop1 = True
stop2 = True
result1 = 0
result2 = 0
active_player = 1

def winner():
    print("Player 1 had a total sum of:", int(result1),"\nPlayer 2 had a total sum of:", result2)
    if result1 > result2:
        print("The winner is player 1 with a total of:", result1)
    elif result2 > result1:
        print("The winner is player 2 with a total of:", result2)
    else:
        print("The game is a tie")

while(stop1 == True or stop2 == True):
    print("Player", active_player," has to choose the move.\n")
    print("The total value for player ", active_player, "at the moment is: ", globals()["result"+str(active_player)], "\n" )
    input_player = input("Please enter the move:\n")
    if input_player == "0":
    # with input == 0 meaning that the player draws a card 
    # and than passes the turn to the next player
        if active_player == 1:
            draw_1, game_deck, player_1_hand = draw(game_deck, player_1_hand)
            result1 += int(l[draw_1,0])
            print("The total value for player 1 is ",result1, "\n")
            if result1 > 21:
                print("Player 1 has a result higher than 21 and lost")
                break
            if stop2 == True:
                active_player = 2
            else:
                active_player = 1
        else:
            draw_1, game_deck, player_2_hand = draw(game_deck, player_2_hand)
            result2 += int(l[draw_1,0])
            print("The total value for player 2 is ",result2, "\n")
            if result2 > 21:
                print("Player 2 has a result higher than 21 and lost")
                break
            if stop1 == True:
                active_player = 1
            else:
                active_player = 2
    elif input_player == "1":
        # with input == 1 is the player to pass his turn forever
        if active_player == 1:    
            stop1 = False
            if stop2 == True:
                active_player = 2
            else:
                winner()
        elif active_player == 2:
            stop2 = False        
            if stop1 == True:
                active_player = 1
            else:
                winner()
    else:
        print("To draw a card type 0, to stay and wait for the end of the game type 1.")
