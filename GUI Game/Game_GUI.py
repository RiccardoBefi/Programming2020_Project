# -*- coding: utf-8 -*-
"""
Created on Fri May  8 12:48:42 2020

@author: leo_b
"""
#CHANGELOG FROM LAST VERSION: BETA THREAD PROCESSING
#(NOW DRAW FUNCTION AND DRAW SOUND HAPPEN AT THE SAME TIME)
#MOVED SOUND TO BUTTONCLICKS INSTEAD OF ACTION FUNCTIONS
from tkinter import *
from PIL import ImageTk, Image
import numpy as np ; import random as rn
import os ; import sys
import re #to find int in strings
from winsound import *
from threading import Thread #still testing

root = Tk()
#root.geometry("1000x770")
#replace previous line with the following for fullscreen
root.overrideredirect(True) ; root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.geometry("1000x800")
root.title("21: The Game") ; root.iconbitmap("ace.ico")

filename = ImageTk.PhotoImage(Image.open("BG\\solid green.png").resize((2000,1100)))
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1) 

#Sounds functions
def exitsound(): PlaySound("Card Sounds\\dieThrow2.mp3", SND_FILENAME)
def drawsound():
    if globals()["MUSIC"]==False:
        PlaySound("Card Sounds\\cardPlace1.mp3", SND_FILENAME)
def staysound():
    if globals()["MUSIC"]==False:
        PlaySound("Card Sounds\\cardShove4.mp3", SND_FILENAME)
def startsound(): PlaySound("Card Sounds\\cardFan1.mp3", SND_FILENAME)

#Loading cards .png
cnames=[None] ; con=0
xdim = 120 ; ydim = round(xdim/0.66); cardsize=(xdim, ydim)
for fname in os.listdir():
    if ".png" in fname:
        name=fname.replace(".png","")
        if "J" in name: name=name.replace("J","11")
        #NOTE: in 21 cards go from 1 to 11
        elif "Q" in name: continue
        elif "K" in name: continue
        elif "A" in name: name=name.replace("A","1")
        globals()[name] = ImageTk.PhotoImage(Image.open(fname).resize(cardsize, Image.ANTIALIAS))
        globals()["L"+name] = Label(image = globals()[name], borderwidth=0,bg="green")
        cnames[con]="L"+name
        cnames = np.append(cnames,[None])
        con += 1
cnames=cnames[:-1]

#Creating game functions (that will be called by buttons)
cpos1 , cpos2 , p1score, p2score = (0,0,0,0) ; turn=True ; nochange=False
activecards1 ,activecards2 = ([None],[None])
red_cards1 ,red_cards2 = ([None],[None])
dstay=0

#Game functions
def ldraw():
    # Thread(target=drawsound).start() #play sound in another thread, \
    #moved to button click
    if(turn): 
        n=1 ; nrow=1            
    else: 
        n=2 ; nrow=3
    
    p = globals()["cpos"+str(n)]+1
    cardname=rn.choice(cnames)
    card=globals()[cardname]
    while(card.winfo_ismapped() == 1): #check if card isn't already there
        cardname=rn.choice(cnames)
        card=globals()[cardname]
        
    if globals()["dstay"] !=1: # If no player stayed, remove the buttons and \
        #cover the cards
        drawcard.grid_forget()
        stay.grid_forget()
        show_cards.grid_forget()
        cover.grid(row=nrow,column=p+1)
    else: # if one of the player stays, only the second player can play. his \
        #covers stay uncovered
        drawcard.grid_forget() ; stay.grid_forget(); show_cards.grid_forget()
        drawcard.grid(row=nrow,column=p+1) ; stay.grid(row=nrow,column=p+2)
    
    globals()["p"+str(n)+"score"]+=int(re.search(r'\d+', cardname).group())
    card.grid(row=nrow,column=p,padx=10,pady=10)
    globals()["cpos"+str(n)] = p
    globals()["activecards"+str(n)][p-1]=cardname
    globals()["red_cards"+str(n)][p-1]=Label(image=red_back,bg="green")
    globals()["activecards"+str(n)]=np.append(globals()["activecards"+str(n)],[None])
    
    globals()["red_cards"+str(n)] = np.append(globals()["red_cards"+str(n)],[None])
    
    globals()["colcount"]=p
    if (nochange==False):
        globals()["turn"]=not(turn) #CHANGE TURN
    
    if globals()["p1score"] > 21:
        # print("player 1 has lost with "+str(globals()["p1score"])+" points")
        #res=Label(globals()["root"],text="player 2 has won with "+str(globals()["p2score"])+" points")
        #res.grid(row=1,column=len(globals()["activecards2"]))
        Label(image=play2win).place(relx=0.6,rely=0.5)
        gover=Label(globals()["root"],image=gameoverpic)
        #gover.grid(row=2,column=len(globals()["activecards2"]),columnspan=10)
        gover.place(relx=0.6,rely=0.3)
        gameover() ; drawcard.grid_forget() ; stay.grid_forget(); cover.grid_forget(); show_cards.grid_forget()
        return
    elif globals()["p2score"] > 21:
        # print("player 2 has lost with "+str(globals()["p2score"])+" points")
        #res=Label(globals()["root"],text="player 1 has won with "+str(globals()["p1score"])+" points")
        #res.grid(row=3,column=len(globals()["activecards1"]))
        Label(image=play1win).place(relx=0.6,rely=0.05)
        gover=Label(globals()["root"],image=gameoverpic)
        gover.place(relx=0.6,rely=0.3)
        gameover() ; drawcard.grid_forget() ; stay.grid_forget(); cover.grid_forget(); show_cards.grid_forget()
        return

def stay(): # The player chooses to stop drawing and pass his turn untill the end of the game
    Thread(target=staysound).start()
    globals()["turn"]=not(turn)
    globals()["nochange"]=not(nochange)
    globals()["dstay"]+=1
    covercards()
    if globals()["dstay"] ==2:
        winstay()
        drawcard.grid_forget() ; stay.grid_forget(); show_cards.grid_forget()
        return
    movebuttons()
        
def winstay():
    if globals()["p1score"] - globals()["p2score"] > 0:
        print("player 1 has won with "+str(globals()["p1score"])+" points")
        res=Label(globals()["root"],text="player 1 has won with "+str(globals()["p1score"])+" points")
        res.grid(row=3,column=len(globals()["activecards2"]))
        #Label(image=winnerpic).grid(row=1,column=len(globals()["activecards1"]))
        Label(image=play1win).place(relx=0.6,rely=0.05)
        gover=Label(globals()["root"],image=gameoverpic)
        gover.place(relx=0.6,rely=0.3)
        gameover()
    elif globals()["p1score"] - globals()["p2score"] < 0:
        print("player 2 has won with "+str(globals()["p2score"])+" points")
        res=Label(globals()["root"],text="player 2 has won with "+str(globals()["p2score"])+" points")
        res.grid(row=1,column=len(globals()["activecards1"]))
        #Label(image=winnerpic).grid(row=3,column=len(globals()["activecards1"]))
        Label(image=play2win).place(relx=0.6,rely=0.05)
        gover=Label(globals()["root"],image=gameoverpic)
        gover.place(relx=0.6,rely=0.3)
        gameover()
    else:
        res=Label(globals()["root"],text="The game is a draw")
        res.grid(row = 2, column = 2)
        gameover()
        
def gameover(): # Game over end screen
    uncover() # Uncover all players cards
    globals()["turn"]=not(turn) #CHANGE TURN
    uncover()
    #turning off buttons
    drawcard.config(state="disabled") ; stay.config(state="disabled"); show_cards.config(state = "disabled")

def movebuttons():
    if(turn):
        pos=1 ; ncol=len(globals()["activecards1"])
    else:
        pos=3 ; ncol=len(globals()["activecards2"])

    if len(globals()["activecards2"]) > 1:
        drawcard.grid_forget(); stay.grid_forget()
        show_cards.grid(row = pos, column = ncol)
    else:
        drawcard.grid(row=pos,column=ncol)
        stay.grid(row=pos,column=ncol+1)

def covercards():
    #this function cover all cards
    for i in range(1,len(globals()["activecards1"])):
        globals()["red_cards1"][i-1].grid(row=1,column=i,padx=10,pady=10)
        
    for i in range(1,len(globals()["activecards2"])):
        globals()["red_cards2"][i-1].grid(row=3,column=i,padx=10,pady=10)
        
    globals()["cover"].grid_forget() #removes the cover button


def uncover():
    # this function uncovers all cards
    show_cards.grid_forget()
    if turn: # Player 1 turn
        ncol = len(globals()["activecards1"]); pos = 1
        show_cards.grid_forget()
        drawcard.grid(row=pos,column=ncol)
        stay.grid(row=pos,column=ncol+1)
        for i in range(0,ncol-1):
            globals()["red_cards1"][i].grid_forget()
            
    else:   # Player 2 turn
        pos=3 ; ncol=len(globals()["activecards2"])
        drawcard.grid(row=pos,column=ncol)
        stay.grid(row=pos,column=ncol+1)
        for i in range(0,ncol-1):
            globals()["red_cards2"][i].grid_forget()

def backtomenu():
    import main_menu

#Background Music Functions
MUSIC=True
def musicoff():
    PlaySound(None, SND_ASYNC)
    globals()["MUSIC"] = not(MUSIC)
    playonbutton()

def musicon(): 
    PlaySound("Card Sounds\\fastinst.wav", SND_FILENAME | SND_ASYNC | SND_ALIAS | SND_LOOP)
    globals()["MUSIC"] = not(MUSIC)
    playoffbutton()

def playonbutton():
    stopmusic.grid_forget()
    playmusic = Button(root, image=redsoundon, command=musicon,bg="green",border=0,
                       cursor="spider")
    playmusic.grid(row=4,column=4)

def playoffbutton():
    stopmusic = Button(root, image=redsoundoff, command=musicoff,bg="green",border=0,
                       cursor="spider")
    stopmusic.grid(row=4,column=4)

def restart_program():
    PlaySound(None, SND_ASYNC)
    os.system("python Game_GUI.py")

#Button images
redquit = ImageTk.PhotoImage(Image.open("Buttons&Labels\\redquit.png"))
redsoundon = ImageTk.PhotoImage(Image.open("Buttons&Labels\\redsoundon.png"))
redsoundoff = ImageTk.PhotoImage(Image.open("Buttons&Labels\\redsoundoff.png"))
redmainmenu = ImageTk.PhotoImage(Image.open("Buttons&Labels\\redmainmenu.png"))
redrestart = ImageTk.PhotoImage(Image.open("Buttons&Labels\\redrestart.png"))
greendraw = ImageTk.PhotoImage(Image.open("Buttons&Labels\\greendraw.png"))
greenstay = ImageTk.PhotoImage(Image.open("Buttons&Labels\\greenstay.png"))
greencover = ImageTk.PhotoImage(Image.open("Buttons&Labels\\greencover.png"))
greenshow = ImageTk.PhotoImage(Image.open("Buttons&Labels\\greenshow.png"))
gameoverpic = ImageTk.PhotoImage(Image.open("Buttons&Labels\\gameoverpic.png").resize((572,104)))
play1win = ImageTk.PhotoImage(Image.open("Buttons&Labels\\play1win.png").resize((572,104)))
play2win = ImageTk.PhotoImage(Image.open("Buttons&Labels\\play2win.png").resize((572,104)))
itsadraw = ImageTk.PhotoImage(Image.open("Buttons&Labels\\itsadraw.png").resize((572,104)))
playimg1 = ImageTk.PhotoImage(Image.open("Buttons&Labels\\player1.png").resize((131,170)))
playimg2 = ImageTk.PhotoImage(Image.open("Buttons&Labels\\player2.png").resize((131,170)))

# Buttons
bh=5 ; bw=20 #button height and button width
exitbutton = Button(root, text="Leave Game", image=redquit, command=lambda:[root.destroy(),exitsound()],
                    bg="green",border=0,cursor="spider")

mainmenu = Button(root, image=redmainmenu, command=lambda:[root.destroy(),exitsound(),backtomenu()],
                  bg="green",border=0,cursor="spider")
drawcard = Button(root, image=greendraw,command=lambda:[ldraw(), Thread(target=drawsound).start()],
                  bg="green",border=0,cursor="spider")
stay = Button(root, image=greenstay,command=stay,bg="green",border=0,
              cursor="spider")
cover=Button(root,image=greencover,command=lambda:[covercards(), movebuttons()],
             bg="green",border=0,cursor="spider")
restart = Button(root,image=redrestart,command=lambda:[root.destroy(),exitsound(),restart_program()],
                 bg="green",border=0,cursor="spider")
show_cards = Button(root, image=greenshow,command=uncover,bg="green",border=0,
                    cursor="spider") #Appears only later in the game
stopmusic = Button(root, image=redsoundoff, command=musicoff,bg="green",border=0,
                   cursor="spider")


#player labels
Label(root,image=playimg1, bg="#66D725",border=0).grid(row=1,column=0,padx=10,pady=20)
Label(root,image=playimg2, bg="#66D725",border=0).grid(row=3,column=0,padx=10,pady=20)
Lred_back.grid(row=2,column=0,padx=10,pady=20)

#Placing buttons within the grid at the start of the game
exitbutton.grid(row=4,column=1)
mainmenu.grid(row=4,column=2)
restart.grid(row=4,column=3)
stopmusic.grid(row=4,column=4)

drawcard.grid(row=1,column=1)
stay.grid(row=1,column=2)

Thread(target=startsound).start()
Thread(target=PlaySound("Card Sounds\\fastinst.wav", SND_FILENAME | SND_ASYNC | SND_ALIAS | SND_LOOP)).start()
root.mainloop()