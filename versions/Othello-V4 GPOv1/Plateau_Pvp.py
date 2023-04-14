#--- Importations ---#
from math import *
from time import *
from random import *

#Init des vars
nodes = 0
moves = 0

#Classe servant a initialiser le plateau de jeu
class Board_pvp:
	def __init__(self):
		#Les blancs d'abord (la val 0 correspond aux blancs/au joueur et vice-versa)
		self.player = 0
		self.passed = False
		self.won = False
		#Init du Plateau
		self.array = []
		for x in range(8):
			self.array.append([])
			for y in range(8):
				self.array[x].append(None)

		#Init des pions de depart
		self.array[3][3] = "w"
		self.array[3][4] = "b"
		self.array[4][3] = "b"
		self.array[4][4] = "w"

		#Raffraichissement du Plateau
		self.oldarray = self.array
	#Init du Plateau

	def update(self):
		from Oth import screen, depth, move
		screen.delete("highlight")
		screen.delete("tile")
		for x in range(8):
			for y in range(8):

				if self.oldarray[x][y] == "w":
					screen.create_oval(54+50*x, 54+50*y, 96+50*x, 96+50*y,
					                   tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
					screen.create_oval(54+50*x, 52+50*y, 96+50*x, 94+50*y,
					                   tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

				elif self.oldarray[x][y] == "b":
					screen.create_oval(54+50*x, 54+50*y, 96+50*x, 96+50*y,
					                   tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
					screen.create_oval(54+50*x, 52+50*y, 96+50*x, 94+50*y,
					                   tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")

		screen.update()
		for x in range(8):
			for y in range(8):

				if self.array[x][y] != self.oldarray[x][y] and self.array[x][y] == "w":
					screen.delete("{0}-{1}".format(x, y))
					#le Plateau a 42 cases, 42/2=21
					for i in range(21):
						screen.create_oval(54+i+50*x, 54+i+50*y, 96-i+50*x, 96 -
						                   i+50*y, tags="tile animated", fill="#000", outline="#000")
						screen.create_oval(54+i+50*x, 52+i+50*y, 96-i+50*x, 94 -
						                   i+50*y, tags="tile animated", fill="#111", outline="#111")
						if i % 3 == 0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					#Agrandissement
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x, 54+i+50*y, 96-i+50*x, 96 -
						                   i+50*y, tags="tile animated", fill="#aaa", outline="#aaa")
						screen.create_oval(54+i+50*x, 52+i+50*y, 96-i+50*x, 94 -
						                   i+50*y, tags="tile animated", fill="#fff", outline="#fff")
						if i % 3 == 0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					screen.create_oval(54+50*x, 54+50*y, 96+50*x, 96+50*y,
					                   tags="tile", fill="#aaa", outline="#aaa")
					screen.create_oval(54+50*x, 52+50*y, 96+50*x, 94+50*y,
					                   tags="tile", fill="#fff", outline="#fff")
					screen.update()

				elif self.array[x][y] != self.oldarray[x][y] and self.array[x][y] == "b":
					screen.delete("{0}-{1}".format(x, y))
					#42/2 = 21
					for i in range(21):
						screen.create_oval(54+i+50*x, 54+i+50*y, 96-i+50*x, 96 -
						                   i+50*y, tags="tile animated", fill="#aaa", outline="#aaa")
						screen.create_oval(54+i+50*x, 52+i+50*y, 96-i+50*x, 94 -
						                   i+50*y, tags="tile animated", fill="#fff", outline="#fff")
						if i % 3 == 0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					#Agrandissement
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x, 54+i+50*y, 96-i+50*x, 96 -
						                   i+50*y, tags="tile animated", fill="#000", outline="#000")
						screen.create_oval(54+i+50*x, 52+i+50*y, 96-i+50*x, 94 -
						                   i+50*y, tags="tile animated", fill="#111", outline="#111")
						if i % 3 == 0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")

					screen.create_oval(54+50*x, 54+50*y, 96+50*x, 96+50*y,
					                   tags="tile", fill="#000", outline="#000")
					screen.create_oval(54+50*x, 52+50*y, 96+50*x, 94+50*y,
					                   tags="tile", fill="#111", outline="#111")
					screen.update()
		#Indique les cases ou le joueur peut placer son pions, a l'aide de mini-cercles ROUGE
		for x in range(8):
			for y in range(8):
				if self.player == 0:
					if valid(self.array, self.player, x, y):
						screen.create_oval(68+50*x, 68+50*y, 32+50*(x+1), 32+50 *
						                   (y+1), tags="highlight", fill="#ff0000", outline="#ff0000")
				elif self.player == 1:
					if valid(self.array, self.player, x, y):
						screen.create_oval(68+50*x, 68+50*y, 32+50*(x+1), 32+50 *
						                   (y+1), tags="highlight", fill="#0df005", outline="#0df005")

		if not self.won:
			#Init les compteurs de points
			self.drawScoreBoard()
			screen.update()
			#Si l'IA fait un move
			if self.player == 1:
				startTime = time()
				self.oldarray = self.array
				alphaBetaResult = self.alphaBeta(
					self.array, depth, -float("inf"), float("inf"), 1)
				self.array = alphaBetaResult[1]

				if len(alphaBetaResult) == 3:
					position = alphaBetaResult[2]
					self.oldarray[position[0]][position[1]] = "b"

				self.player = 1-self.player
				deltaTime = round((time()-startTime)*100)/100
				if deltaTime < 2:
					sleep(2-deltaTime)
				nodes = 0
				#Le joueur veut-il passer son tour?
				self.passTest()
		else:
			screen.create_text(250, 550, anchor="c", font=(
				"Consolas", 15), text="La partie est terminee... (GAME OVER!)")



    
	def play(self):
		while not self.won:
			# Afficher le plateau et les informations sur le joueur
			self.update()
			print(f"Joueur {self.player}, à vous de jouer !")

			# Obtenir les coordonnées de la case choisie par le joueur
			valid_move = False
			while not valid_move:
				try:
					x, y = map(int, input("Entrez les coordonnées (x,y) de votre coup : ").split(','))
				except ValueError:
					print("Coordonnées invalides, veuillez réessayer.")
					continue

				if self.is_valid_move(x, y):
					valid_move = True
				else:
					print("Coup invalide, veuillez réessayer.")

			# Jouer le coup choisi par le joueur
			self.make_move(x, y)

			# Vérifier si le joueur suivant peut jouer ou s'il a gagné
			if self.is_game_over():
				self.won = True
				print(f"Le joueur {self.player} a gagné !")
			elif self.is_player_stuck():
				self.passed = True
				print(f"Le joueur {self.player} doit passer son tour.")
			else:
				self.switch_player()

	# Changer le joueur actuel
	def switch_player(self):
		self.player = 1 - self.player
		self.passed = False

	# Vérifier si le coup est valide pour le joueur actuel
	def is_valid_move(self, x, y):
		if self.array[x][y] is not None:
			return False
		if not self.is_valid_direction(x, y):
			return False
		return True

	# Jouer le coup et met à jour le plateau
	def make_move(self, x, y):
		self.array[x][y] = self.player_color()
		self.flip_pieces(x, y)
		self.oldarray = self.array

	# Vérifier si le jeu est terminé
	def is_game_over(self):
		if self.is_board_full():
			return True
		if self.is_player_stuck() and self.passed:
			return True    



	#Deplace a la position
	def boardMove(self, x, y):
		from Oth import move
		global nodes
		#Fait le deplacement et raffraichit la fenetre (de l'app, au cas ou certains auraient un peu de mal...)
		if self.player == 0: 
			self.oldarray = self.array
			self.oldarray[x][y] = "w"
			self.array = move(self.array, x, y)
		elif self.player == 1: 
			self.oldarray = self.array
			self.oldarray[x][y] = "b "
			self.array = move(self.array, x, y)

		#Changement de joueur
		self.player = 1-self.player
		self.update()

		#Verifie si l'IA prefere passer son tour
		self.passTest()
		self.update()

	#METHODE: Ecris le tableau de score dans la fenetre (en temps reel)
	def drawScoreBoard(self):
		from GUI import screen
		global moves
		#Deleting prior score elements
		screen.delete("score")

		#Score base sur le nombre de case appartenant au joueur/a l'IA
		player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y] == "w":
					player_score += 1
				elif self.array[x][y] == "b":
					computer_score += 1

		if self.player == 0:
			player_colour = "red"
			computer_colour = "green"
		else:
			player_colour = "red"
			computer_colour = "green"

		screen.create_oval(5, 540, 25, 560, fill=player_colour,
		                   outline=player_colour)
		screen.create_oval(380, 540, 400, 560, fill=computer_colour,
		                   outline=computer_colour)

		#Pushing text to screen
		screen.create_text(30, 550, anchor="w", tags="score", font=(
			"Consolas", 50), fill="white", text=player_score)
		screen.create_text(400, 550, anchor="w", tags="score", font=(
			"Consolas", 50), fill="black", text=computer_score)

		moves = player_score+computer_score

	#METHOD: Demande si le joueur veut passer, si oui, changement de joueur
	def passTest(self):
		mustPass = True
		for x in range(8):
			for y in range(8):
				if valid(self.array, self.player, x, y):
					mustPass = False
		if mustPass:
			self.player = 1-self.player
			if self.passed == True:
				self.won = True
			else:
				self.passed = True
			self.update()
		else:
			self.passed = False


#Fonctions necessaires a la mise en place d'une partie d'Othello en python
def dumbScore(array, player):
	score = 0
	#Met en place les couleurs des joueurs
	if player == 1:
		colour = "b"
		opponent = "w"
	else:
		colour = "w"
		opponent = "b"
	#+1 si couleur du joueur, -1 si couleur de l'opposant
	for x in range(8):
		for y in range(8):
			if array[x][y] == colour:
				score += 1
			elif array[x][y] == opponent:
				score -= 1
	return score
def slightlyLessDumbScore(array, player):
	score = 0
	#Met en place les couleurs des joueurs
	if player == 1:
		colour = "b"
		opponent = "w"
	else:
		colour = "w"
		opponent = "b"
	#Etudie les cases du plateau pour compter le score
	for x in range(8):
		for y in range(8):

			add = 1
			
			if (x == 0 and 1 < y < 6) or (x == 7 and 1 < y < 6) or (y == 0 and 1 < x < 6) or (y == 7 and 1 < x < 6):
				add = 3
			
			elif (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
				add = 5
			
			if array[x][y] == colour:
				score += add
			elif array[x][y] == opponent:
				score -= add
	return score
def decentHeuristic(array, player):
	score = 0
	cornerVal = 25
	adjacentVal = 5
	sideVal = 5
	#Met en place les couleurs des joueurs
	if player == 1:
		colour = "b"
		opponent = "w"
	else:
		colour = "w"
		opponent = "b"
	#Etudie les cases du plateau pour compter le score
	for x in range(8):
		for y in range(8):
			
			add = 1

			
			if (x == 0 and y == 1) or (x == 1 and 0 <= y <= 1):
				if array[0][0] == colour:
					add = sideVal
				else:
					add = -adjacentVal

			elif (x == 0 and y == 6) or (x == 1 and 6 <= y <= 7):
				if array[7][0] == colour:
					add = sideVal
				else:
					add = -adjacentVal

			elif (x == 7 and y == 1) or (x == 6 and 0 <= y <= 1):
				if array[0][7] == colour:
					add = sideVal
				else:
					add = -adjacentVal

			elif (x == 7 and y == 6) or (x == 6 and 6 <= y <= 7):
				if array[7][7] == colour:
					add = sideVal
				else:
					add = -adjacentVal

			
			elif (x == 0 and 1 < y < 6) or (x == 7 and 1 < y < 6) or (y == 0 and 1 < x < 6) or (y == 7 and 1 < x < 6):
				add = sideVal
			
			elif (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
				add = cornerVal
			
			if array[x][y] == colour:
				score += add
			elif array[x][y] == opponent:
				score -= add
	return score
def finalHeuristic(array, player):
	if moves <= 8:
		numMoves = 0
		for x in range(8):
			for y in range(8):
				if valid(array, player, x, y):
					numMoves += 1
		return numMoves+decentHeuristic(array, player)
	elif moves <= 52:
		return decentHeuristic(array, player)
	elif moves <= 58:
		return slightlyLessDumbScore(array, player)
	else:
		return dumbScore(array, player)
def valid(array, player, x, y):
	#Init couleur joueur
	if player == 0:
		colour = "w"
	else:
		colour = "b"

	#Move invalide si la case n'est pas prenable
	if array[x][y] != None:
		return False

	else:
		#Genere les cases_disponibles/ou l'on puisse jouer
		neighbour = False
		neighbours = []
		for i in range(max(0, x-1), min(x+2, 8)):
			for j in range(max(0, y-1), min(y+2, 8)):
				if array[i][j] != None:
					neighbour = True
					neighbours.append([i, j])
		#Move invalide si ce n'est pas une cases_disponibles
		if not neighbour:
			return False
		else:
			#Interragit pour savoir combien de pions doivent etre places en fonction du coup
			valid = False
			for neighbour in neighbours:

				neighX = neighbour[0]
				neighY = neighbour[1]

				
				if array[neighX][neighY] == colour:
					continue
				else:
					#Determine la direction de la ligne
					deltaX = neighX-x
					deltaY = neighY-y
					tempX = neighX
					tempY = neighY

					while 0 <= tempX <= 7 and 0 <= tempY <= 7:
						
						if array[tempX][tempY] == None:
							break
						
						if array[tempX][tempY] == colour:
							valid = True
							break
						
						tempX += deltaX
						tempY += deltaY
			return valid
def drawGridBackground(outline=False):
	from GUI import screen
	#If we want an outline on the board then draw one
	if outline:
		screen.create_rectangle(50, 50, 450, 450, outline="#111")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		screen.create_line(50, lineShift, 450, lineShift, fill="#111")

		#Vertical line
		screen.create_line(lineShift, 50, lineShift, 450, fill="#111")

	screen.update()

