# -*- coding: utf-8 -*-
"""
Created on Mon May 18 16:59:42 2020

@author: paedr
"""

#CHANGELOG FROM LAST VERSION: BETA THREAD PROCESSING
#(NOW DRAW FUNCTION AND DRAW SOUND HAPPEN AT THE SAME TIME)
#MOVED SOUND TO BUTTONCLICKS INSTEAD OF ACTION FUNCTIONS
from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image, ImageFilter, ImageDraw
import numpy as np ; import random as rn
import os
import sys
import re #to find int in strings
from winsound import *
from threading import Thread #still testing
import threading
import time

root = Tk()
root.configure(background='green')
#root.geometry("1000x800")
#replace previous line with the following for fullscreen
root.overrideredirect(True) ; root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("Main Menu") ; root.iconbitmap("ace.ico")
bgx=1800 ; bgy=round(bgx/1.78) ; bgsize=(bgx,bgy)
filename = ImageTk.PhotoImage(Image.open("BG\\whisky.png").resize(bgsize))
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1) 


#Sounds functions
def exitsound(): PlaySound("Card Sounds\\dieThrow2.mp3", SND_FILENAME)

#Button functions
def startBlackJack():
    PlaySound(None, SND_ASYNC)
    os.system("python Black_Jack.py")

def startGameGUI():
    PlaySound(None, SND_ASYNC)
    os.system("python Game_GUI.py")
    
#button images (casino chips)
size=150 ; chipsize=(size,size)
redchipBJ = ImageTk.PhotoImage(Image.open("Buttons&Labels\\redchipBJ.png").resize(chipsize, Image.ANTIALIAS))
redchipquit = ImageTk.PhotoImage(Image.open("Buttons&Labels\\redchipquit.png").resize(chipsize, Image.ANTIALIAS))
blackchip21 = ImageTk.PhotoImage(Image.open("Buttons&Labels\\blackchip21.png").resize(chipsize, Image.ANTIALIAS))
blackchipOFF = ImageTk.PhotoImage(Image.open("Buttons&Labels\\blackchipOFF.png").resize(chipsize, Image.ANTIALIAS))
blackchipON = ImageTk.PhotoImage(Image.open("Buttons&Labels\\blackchipON.png").resize(chipsize, Image.ANTIALIAS))


#Background Music Functions
valx=0.08;valy=0.53
def musicoff():
    PlaySound(None, SND_ASYNC)
    playonbutton()

def musicon(): 
    PlaySound("Card Sounds\\fast.wav", SND_FILENAME | SND_ASYNC | SND_ALIAS)
    playoffbutton()

def playonbutton():
    #stopmusic.place_forget()
    playmusic = Button(root, text="Music ON", image=blackchipON, command=musicon,
                       bg="black",borderwidth=0,cursor="spider")
    playmusic.place(anchor=CENTER,relx=valx,rely=valy)

def playoffbutton():
    stopmusic = Button(root, text="Music OFF", image=blackchipOFF, command=musicoff,
                      bg="black",borderwidth=0,cursor="spider")
    stopmusic.place(anchor=CENTER,relx=valx,rely=valy)

#Main Title
logox = 640 ; logoy = round(logox/4.2) ; logosize=(logox,logoy)
logo = ImageTk.PhotoImage(Image.open("Frame\\mainlogo\\logo.png").resize(logosize, Image.ANTIALIAS))
Label(image=logo,bg="black",borderwidth=0).place(anchor=CENTER,relx=0.23,rely=0.13)


#Buttons
BJ = Button(root, text = "Play Black Jack", image=redchipBJ, command= lambda:[root.destroy(),startBlackJack()],
            bg="black",borderwidth=0,cursor="spider")
BJ.place(anchor=CENTER,relx=0.08,rely=0.32)
Game_Gui = Button(root, text = "Play 21", image=blackchip21, command= lambda:[root.destroy(),startGameGUI()],
                  bg="black",borderwidth=0,cursor="spider")
Game_Gui.place(anchor=CENTER,relx=0.2,rely=0.32)
exitbutton = Button(root, text="Leave Game", image=redchipquit, command=lambda:[root.destroy(),exitsound()],
                    bg="black",borderwidth=0,cursor="spider")
exitbutton.place(anchor=CENTER,relx=0.08,rely=0.76)
stopmusic = Button(root, text="Music OFF", image=blackchipOFF, command=musicoff,
                   bg="black",borderwidth=0,cursor="spider")
stopmusic.place(anchor=CENTER,relx=valx,rely=valy)


PlaySound("Card Sounds\\fast.wav", SND_FILENAME | SND_ASYNC | SND_ALIAS | SND_LOOP)
root.mainloop()