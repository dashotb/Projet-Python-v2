from tkinter import *
from math import *
from time import *
from random import *


#Mise en place de Tkinter
root = Tk()
screen = Canvas(root, width=500, height=600,
                background="#c0c6c8", highlightthickness=0)
screen.pack()


def keyHandle(event):
	from Oth import root, playGame
	symbol = event.keysym
	if symbol.lower() == "r":
		playGame()
	elif symbol.lower() == "q":
		root.destroy()


def create_buttons():
	#Boutton Relancer
	#Background/shadow
	screen.create_rectangle(0, 5, 50, 55, fill="#000033", outline="#000033")
	screen.create_rectangle(0, 0, 50, 50, fill="#000088", outline="#000088")

	#Fleche
	screen.create_arc(5, 5, 45, 45, fill="#000088", width="2",
	                  style="arc", outline="white", extent=300)
	screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

	#Boutton Quitter
	#Background/shadow
	screen.create_rectangle(450, 5, 500, 55, fill="#330000", outline="#330000")
	screen.create_rectangle(450, 0, 500, 50, fill="#880000", outline="#880000")
	#Croix
	screen.create_line(455, 5, 495, 45, fill="white", width="3")
	screen.create_line(495, 5, 455, 45, fill="white", width="3")


from Oth import clickHandle
#Binding, Reglages
screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>", keyHandle)
screen.focus_set()

#Let's Go
root.wm_title("Othello par les Eleves de L1-Info a Champo: HABIB & nour")
root.mainloop()
