# -*- coding: utf-8 -*-
"""
Created on Wed May 20 08:34:38 2020

@author: leo_b
"""

from tkinter import *
from PIL import ImageTk, Image

#Button images
redquit = ImageTk.PhotoImage(Image.open("Frame\\redquit.png"))
redsoundon = ImageTk.PhotoImage(Image.open("Frame\\redsoundon.png"))
redsoundoff = ImageTk.PhotoImage(Image.open("Frame\\redsoundoff.png"))
redmainmenu = ImageTk.PhotoImage(Image.open("Frame\\redmainmenu.png"))
redrestart = ImageTk.PhotoImage(Image.open("Frame\\redrestart.png"))
greendraw = ImageTk.PhotoImage(Image.open("Frame\\greendraw.png"))
greenstay = ImageTk.PhotoImage(Image.open("Frame\\greenstay.png"))
greencover = ImageTk.PhotoImage(Image.open("Frame\\greencover.png"))
greenshow = ImageTk.PhotoImage(Image.open("Frame\\greenshow.png"))
gameoverpic = ImageTk.PhotoImage(Image.open("Frame\\gameoverpic.png").resize((572,104)))
winnerpic = ImageTk.PhotoImage(Image.open("Frame\\greenwinner.png").resize((572,104)))
