# -*- coding: utf-8 -*-
"""
Created on Sun May 17 16:22:36 2020

@author: paedr
"""


from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import numpy as np ; import random as rn
import os
import re #to find int in strings
from winsound import *
from threading import Thread #still testing

# Create the playing field
root = Tk()
root.configure(background='green')
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("BlackJack") ; root.iconbitmap("ace.ico")

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

#Loading cards .png and changing the values
cnames=[None] ; con=0
xdim = 120 ; ydim = round(xdim/0.66); cardsize=(xdim, ydim)
for fname in os.listdir():
    if ".png" in fname:
        name=fname.replace(".png","")
        if "J" in name: name=name.replace("J","10J")
        elif "Q" in name: name=name.replace("Q","10Q")
        elif "K" in name: name=name.replace("K","10K")
        elif "A" in name: name=name.replace("A","1")
        globals()[name] = ImageTk.PhotoImage(Image.open(fname).resize(cardsize, Image.ANTIALIAS))
        globals()["L"+name] = Label(image = globals()[name], border=0,bg="green")
        cnames[con]="L"+name
        cnames = np.append(cnames,[None])
        con += 1
cnames=cnames[:-1]

# Create player variables
#Creating game functions (that will be called by buttons)
cpos1 , cpos2, cpos3, p1score, p2score, p3score = (0,0,0,0,0,0) ; turn=1 ; nochange=False
activecards1 ,activecards2, activecards3 = ([None],[None], [None])
red_cards1,red_cards2 = ([None],[None])
bust=0
players = 3

# Game function
def draw():
    #Thread(target=drawsound).start() #play sound in another thread
    if(globals()["turn"] < globals()["players"]): 
        n = globals()["turn"] ; nrow=globals()["turn"] + 2      
    else:
        n = 3; nrow = 1
    
    p = globals()["cpos"+str(n)]+1
    cardname=rn.choice(cnames)
    card=globals()[cardname]
    while(card.winfo_ismapped() == 1): #check if card isn't already there
        print(card.winfo_ismapped() == 1)
        cardname=rn.choice(cnames)
        card=globals()[cardname]
    
    globals()["p"+str(n)+"score"]+=int(re.search(r'\d+', cardname).group())
    card.grid(row=nrow,column=p,padx=10,pady=10)
    globals()["cpos"+str(n)] = p
    globals()["activecards"+str(n)][p-1]=cardname
    globals()["activecards"+str(n)]=np.append(globals()["activecards"+str(n)],[None])

    if globals()["p"+str(n)+"score"] > 21:
        res = Label(globals()["root"],text="player "+str(n)+" went bust")
        res.grid(row=nrow,column=1)
        #globals()["bust"] += 1
        stay_decision()
    return

def win_decision():
    for n in range(1, globals()["players"]):
        # print(n)
        if globals()["p"+str(n)+"score"] - globals()["p3score"] > 0 and globals()["p"+str(n)+"score"] <=21 and globals()["p3score"]<=21:
            #res=Label(globals()["root"],text="Player "+str(n)+" has won with "+str(globals()["p"+str(n)+"score"])+" points")
            #res.grid(row = n+2, column = len(globals()["activecards"+str(n)]))
            Label(image=globals()["play"+str(n)+"win"]).place(relx=0.6,rely=n/3+0.2)
        elif globals()["p"+str(n)+"score"] <=21 and globals()["p3score"] > 21:
            #res=Label(globals()["root"],text="Player "+str(n)+" has won with "+str(globals()["p"+str(n)+"score"])+" points")
            #res.grid(row = n+2, column = len(globals()["activecards"+str(n)]))
            Label(image=globals()["play"+str(n)+"win"]).place(relx=0.6,rely=n/3+0.2)
        else:
            #res=Label(globals()["root"],text="The table has won")
            #res.grid(row = n+2, column = len(globals()["activecards"+str(n)]))
            Label(image=dealerwins).place(relx=0.6,rely=0.2)
    gameover()
        
def gameover():
    for t in range(1, globals()["players"]): # removes the covering from the cards
        if type(globals()["red_cards" + str(t)]) == list:
            continue;
        else:
            globals()["red_cards" + str(t)].grid_forget()
    drawcard.grid_forget() ; stay.grid_forget()
    gover=Label(globals()["root"],image=gameoverpic)
    #gover.grid(row=1,column=len(globals()["activecards3"]))
    gover.place(relx=0.6,rely=0.05)

def stay_decision():
    if globals()["turn"] == globals()["players"]-1: # Turn of the table: automatic
        globals()["turn"] += 1
        if globals()["bust"] < globals()["players"]-1:
            while p3score <= 16:
                draw()
        else:
            res = Label(globals()["root"],text="The table won")
            res.grid(row=globals()["turn"]+2,column=1)
        win_decision()
    else:
        covercards()
        globals()["turn"] += 1
    return

def covercards(): # function to cover the last drawn card, so the other players do not know them
    if globals()["turn"] == 1:
        globals()["red_cards1"] = Label(image=red_back,bg="green")
        globals()["red_cards1"].grid(row=3,column=len(globals()["activecards1"])-1,padx=10,pady=10)
    elif globals()["turn"] == 2:
        globals()["red_cards2"] = Label(image=red_back,bg="green")
        globals()["red_cards2"].grid(row=4,column=len(globals()["activecards2"])-1,padx=10,pady=10)
    
def backtomenu():
    os.system("python main_menu.py")

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
    playmusic.grid(row=2,column=6)

def playoffbutton():
    stopmusic = Button(root, image=redsoundoff, command=musicoff,bg="green",border=0,
                       cursor="spider")
    stopmusic.grid(row=2,column=6)

def restart_program():
    PlaySound(None, SND_ASYNC)
    os.system("python Black_Jack.py")

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
dealerimg = ImageTk.PhotoImage(Image.open("Buttons&Labels\\dealerimg.png").resize((131,170)))

dealerwins = ImageTk.PhotoImage(Image.open("Buttons&Labels\\dealerwins.png").resize((572,104)))

# Buttons
bh=5 ; bw=15 #button height and button width
exitbutton = Button(root, text="Leave Game", image=redquit, command=lambda:[root.destroy(),exitsound()],
                    bg="green",border=0,cursor="spider")
mainmenu = Button(root, image=redmainmenu, command=lambda:[root.destroy(),exitsound(),backtomenu()],
                  bg="green",border=0,cursor="spider")
drawcard = Button(root, image=greendraw,command=lambda:[draw(), Thread(target=drawsound).start()],
                  bg="green",border=0,cursor="spider")
stay = Button(root, image=greenstay,command=lambda:[stay_decision(), Thread(target=staysound).start()],
                  bg="green",border=0,cursor="spider")
restart = Button(root,image=redrestart,command=lambda:[root.destroy(),exitsound(),restart_program()],
                 bg="green",border=0,cursor="spider")
stopmusic = Button(root, image=redsoundoff, command=musicoff,bg="green",border=0,
                   cursor="spider")

# Player labels and borders
goldframe=ImageTk.PhotoImage(Image.open("Frame\\Framezz.png").resize((100,50))) 
Label(image=goldframe,bg="white",borderwidth=0).grid(row=1,column=0,padx=10,pady=90)
Label(image=goldframe,bg="white",borderwidth=0).grid(row=3,column=0,padx=10,pady=90)
Label(image=goldframe,bg="white",borderwidth=0).grid(row=4,column=0,padx=10,pady=10)

fontstyle = tkFont.Font(family="Gabriola", size=13, weight="bold")
Label(root,image=dealerimg, bg="#66D725",border=0).grid(row=1,column=0,padx=10,pady=20)
Label(root,image=playimg1, bg="#66D725",border=0).grid(row=3,column=0,padx=10,pady=20)
Label(root,image=playimg2, bg="#66D725",border=0).grid(row=4,column=0,padx=10,pady=20)

Lred_back.grid(row=2,column=0,padx=10,pady=20)

#Placing buttons within the grid at the start of the game
exitbutton.grid(row=2,column=3)
mainmenu.grid(row=2,column=4)
restart.grid(row=2,column=5)
stopmusic.grid(row=2,column=6)
drawcard.grid(row=2,column=1)
stay.grid(row=2,column=2)


Thread(target=startsound).start()
Thread(target=PlaySound("Card Sounds\\fastinst.wav", SND_FILENAME | SND_ASYNC | SND_ALIAS | SND_LOOP)).start()

root.mainloop()