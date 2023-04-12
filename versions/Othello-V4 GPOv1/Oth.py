#--- Importations ---#
from GUI import root, screen
from tkinter import *
from copy import deepcopy
 
#Init de la var depth
depth = 4


#Les fonctions suivantes sont ici a cause des vars global depth, board
def clickHandle(event):
	from Plateau import valid
	global depth
	xMouse = event.x
	yMouse = event.y
	if running:
		if xMouse >= 450 and yMouse <= 50:
			root.destroy()
		elif xMouse <= 50 and yMouse <= 50:
			playGame()
		else:
			#A qui le tour?
			if board.player == 0:
				#Supprime les reccords
				x = int((event.x-50)/50)
				y = int((event.y-50)/50)

				#Interragit avec le clique du joueur, en fonction d'ou le joueur souhaite poser son pion
				if 0 <= x <= 7 and 0 <= y <= 7:
					if valid(board.array, board.player, x, y):
						board.boardMove(x, y)
	else:
		#Choix du mode de jeu avec les coordonnes du clique de la souris dans la fenetre
		if 300 <= yMouse <= 350:
			#PvP
			if 25 <= xMouse <= 155:
				depth = 2
				board.play()
			#PvC (Player vs Computer) 2 etoiles/normal
			elif 180 <= xMouse <= 310:
				depth = 4
				playGame()
			#PvC 3 etoiles/difficile
			elif 335 <= xMouse <= 465:
				depth = 6
				playGame()
		#PS: On aime pas trop quand c'est facile
def move(passedArray, x, y):
	#Cette fonction permet de savoir quels sont les cases sur lequelles on puisse jouer
	global board
	array = deepcopy(passedArray)
	if board.player == 0:
		colour = "w"

	else:
		colour = "b"
	array[x][y] = colour

	neighbours = []
	for i in range(max(0, x-1), min(x+2, 8)):
		for j in range(max(0, y-1), min(y+2, 8)):
			if array[i][j] != None:
				neighbours.append([i, j])

	convert = []

	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]

		if array[neighX][neighY] != colour:
			path = []

			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			while 0 <= tempX <= 7 and 0 <= tempY <= 7:
				path.append([tempX, tempY])
				value = array[tempX][tempY]

				if value == None:
					break
				if value == colour:
					for node in path:
						convert.append(node)
					break
				tempX += deltaX
				tempY += deltaY

	for node in convert:
		array[node[0]][node[1]] = colour

	return array

#Fonctions pour lancer  une Partie
def runGame():
	#Fonction permettant de choisir le mode de jeu
	global running
	running = False
	i=0
	#Titre et ombres
	screen.create_text(250, 203, anchor="c", text="Reversi",
	                   font=("Consolas", 20), fill="#aaa")
	screen.create_text(250, 200, anchor="c", text="Reversi",
	                   font=("Consolas", 20), fill="#f26868")
	
	#Case de gauche (vide en attendant le mode Pvp)
	#Background
	screen.create_rectangle(25+155*i, 310, 155+155*i, 355,
                         fill="#828788", outline="#828788")
	screen.create_rectangle(25+155*i, 300, 155+155*i, 350,
                         fill="#f26868", outline="#f26868")

	#Cases avec etoiles (niveaux de difficulte du bot)
	for i in range(2):
		i += 1
		#Background
		screen.create_rectangle(25+155*i, 310, 155+155*i, 355,
		                        fill="#828788", outline="#828788")
		screen.create_rectangle(25+155*i, 300, 155+155*i, 350,
		                        fill="#f26868", outline="#f26868")

		spacing = 130/(i+2)
		for x in range(i+1):
			#Affichages des Etoiles+Ombres
			screen.create_text(25+(x+1)*spacing+155*i, 326, anchor="c",
			                   text="\u2605", font=("Consolas", 25), fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i, 327, anchor="c",
			                   text="\u2605", font=("Consolas", 25), fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i, 325, anchor="c",
			                   text="\u2605", font=("Consolas", 25), fill="#ffd700")
		
	

	screen.update()
def playGame():
	from Plateau import Board, drawGridBackground
	from GUI import create_buttons
	global board, running
	running = True
	screen.delete(ALL)
	create_buttons()
	board = 0

	#Dessine la grille du plateau de jeu
	drawGridBackground()

	#Cree le Plateau + MaJ
	board = Board()
	board.update()

runGame()

