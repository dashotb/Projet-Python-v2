#=======================================================PARTIE 1=================================================================
#=======================================================EX1======================================================================

def indice_valide(plateau,indice) : #indice valide dans le plateau
    return (indice <= plateau["n"]-1) and (indice >= 0)


#=======================================================EX2======================================================================

def case_valide(plateau, i, j) :    #case existante où pas
    p = plateau["n"]
    return (i < p) and (j < p) and (i >= 0) and (j >= 0)

#=======================================================EX3======================================================================

def get_case(plateau,i,j) :         # permet d'obtenir l'indice de la case rechercher
    tab = plateau["case"]
    taille = plateau["n"]
    if not case_valide(plateau ,i,j) :
        return False
    return tab[taille*i+j]              # i = lignes // j = Colonnes

#=======================================================EX4======================================================================

def set_case(plateau,i,j,val) :     #met un pion
    if case_valide(plateau,i,j):
        if (val == 0) or (val == 1) or (val == 2) :
            indice = plateau["n"]*i+j
            plateau["case"][indice] = val
            return plateau,True
    return False
#=======================================================EX5======================================================================
def creer_plateau(n) :              #creation du plateau
    plateau={"n":n, "case":[]}
    if n!=4 and n!=6 and n!=8:
        return False
    taille=n*n
    i=0
    tab=[]
    while i<taille:                  #boucle qui cree le tableau
        tab.append(0)
        i+=1
    plateau["case"]=tab     #insertion dans le dico plateau
    if n==4:        #different type de plateau
        i=0
        j=0
    if n==6:
        i=1
        j=1
    if n==8:
        i=2
        j=2
    set_case(plateau,i+1,j+1,2)         #initialisation des pions de bases
    set_case(plateau,i+1,j+2,1)
    set_case(plateau,i+2,j+1,1)
    set_case(plateau,i+2,j+2,2)
    return plateau
#=======================================================EX6======================================================================
def afficher_plateau1(plateau):
    i=0
    compteur=0                  #compteur pour calcule le nombre de valeur present sur le tableau
    while i < len(plateau["case"]):
        print(plateau["case"][i], end=' ')      #end='' permet de print sur une ligne
        if compteur == plateau["n"]-1:          #limite le nombre de valeur sur un ligne par n
            print("\n")                         #retour a la ligne
            compteur=-1
        compteur+=1
        i+=1

def afficher_plateau2(plateau):
    i=0
    compteur=0                  #compteur pour calcule le nombre de valeur present sur le tableau
    compteurligne=0             #compteur de ligne
    ligne="*******"
    colone="*      "
    print(ligne*plateau["n"]+"*", end=''"\n")       #contour en haut du tableau
    print(colone*(plateau["n"]+1))                  #premier colone
    print("*  ", end='')
    while i < len(plateau["case"]):
        if plateau["case"][i]==0:    #changement indice en pion(couleur)
            print(" ", end=' ')      #end='' permet de print sur une ligne
        elif plateau["case"][i]==1:   #changement indice en pion(couleur)
            print("N ", end='')
        else :                          #changement indice en pion(couleur)
            print("B ", end='')
        print("  *  ", end='')                  #colone
        if compteur == plateau["n"]-1:          #limite le nombre de valeur sur un ligne par n
            print("\r")                         #retour a la ligne sans saut de ligne
            print(colone*(plateau["n"]+1))      #colone
            print(ligne*plateau["n"]+"*", end=''"\n")   #fin de ligne
            compteurligne+=1
            if compteurligne <= plateau["n"]-1:
                print(colone*(plateau["n"]+1))
                print("*  ", end='')
            compteur=-1
        compteur+=1
        i+=1


#==========================================================PARTIE2==================================================================================
#===========================================================EX7=====================================================================================
def pion_adverse(joueur) :  #retour le joueur adverse
    if joueur == 1 :
        return 2
    elif joueur == 2 :
        return 1
    return False

#================================================================EX8====================================================================================
def prise_possible_direction(plateau, i, j, vertical, horizontal, joueur) : #Teste si la direction donnée est possible pour manger le pion adverse
    if vertical == 0 and horizontal == 0 :              #position de base donc False
        return False
    if not case_valide(plateau, i, j):
        return False
    x = pion_adverse(joueur)
    xvertical = i + vertical                               #calcule position
    yhorizontal = j + horizontal                           #calcule position
    while get_case(plateau, xvertical, yhorizontal) == x : # si la conditon est valide alors il y a un pion adverse adjacent
        xvertical += vertical
        yhorizontal += horizontal
        if get_case(plateau, xvertical, yhorizontal) == 0 : # si la case suivante est vide, ne mange pas de pion
            return False
        if get_case(plateau, xvertical, yhorizontal) == joueur : # si la case suivant contient un pion alie, mange le pion
            return True
    return False


#=================================================================EX9============================================================
def mouvement_valide(plateau, i, j , joueur) : #est ce qu'on peut pose un pion ( peut importe la direction )
    vertical = -1
    while vertical <= 1 :                              #test toute les direction
        horizontal = -1
        while horizontal <= 1 :
            if prise_possible_direction(plateau, i, j, vertical, horizontal, joueur) :
                return True
            horizontal += 1                 #change les directions
        vertical += 1                       #change les directions
    return False

#=================================================================EX10============================================================
def mouvement_direction(plateau, i, j, vertical, horizontal , joueur) : #change les pion adverse qui sont manger dans la direction
    if mouvement_valide(plateau, i, j,joueur) :
        i += vertical                                       #calcule nouvelle position
        j += horizontal                                     #calcule nouvelle position
        while get_case(plateau, i, j) != joueur  :          #met le pion
            set_case(plateau,i,j,joueur)
            i += vertical
            j += horizontal
#=================================================================EX11============================================================
def mouvement(plateau, i, j, joueur) : # Si direction valide et que on peut placer pion, place le pion
    if mouvement_valide(plateau, i, j , joueur) and get_case(plateau,i,j)==0 :
        set_case(plateau, i, j, joueur)                       #Place pions
        vertical = -1
        while vertical <= 1 :
            horizontal = -1
            while horizontal <= 1 :
                if prise_possible_direction(plateau, i, j, vertical, horizontal, joueur) :
                    mouvement_direction(plateau, i , j , vertical , horizontal , joueur)    #retourne pion adverse
                horizontal += 1
            vertical += 1
#=================================================================EX12============================================================
def joueur_peut_jouer(plateau,joueur) : #cherche dans toute les cases un mouvement possible
    i = 0
    while i < plateau["n"] :
        j = 0
        while j < plateau["n"] :
            if mouvement_valide(plateau, i , j, joueur) and get_case(plateau,i,j)==0 :
                return True
            j+=1
        i+=1
    return False

#=================================================================EX13============================================================
def fin_de_partie(plateau) : #si personne peut jouer, fin de partie
    if joueur_peut_jouer(plateau,1) == False and joueur_peut_jouer(plateau,2) == False :
        return True
    return False

#=================================================================EX14============================================================
def gagnant(plateau) : #compare le score
    i = 0
    score1 = 0
    score2 = 0
    while i < len(plateau["case"]) :
        if plateau["case"][i] == 1 :       #calcule le score1
            score1+=1
        elif plateau["case"][i] == 2 :     #calcule le score2
            score2+=1
        i+=1
    if score1 > score2 :    #Retourne 2 si le joueur 2 a gagné
        return "N"
    elif score2 > score1 :  #Retourne 2 si le joueur 2 a gagné
        return "B"
    else :
        return "egalité"

#===================================Partie 3=======================================================
#15
def creer_partie(n):
    partie={}
    plateau = creer_plateau(n)  #Créer une partie
    partie["joueur"]=1
    partie["plateau"]=plateau
    return partie

#16
def saisie_valide(partie, s):
    if str(s)=="M" or str(s)=="m":
        return True     # si le joueur tape M ou m, on return True
    ascii=ord(s[0])
    i=ord(s[0])-97          #convertie
    j=int(s[1])-1           #convertie
    if partie["plateau"]["n"]==4 :
        if ascii>=97 and ascii<=100 and int(s[1])>=1 and int(s[1])<=4:  #verifie la validite des coordonnée
            return True
    elif partie["plateau"]["n"]==6 :
        if ascii>=97 and ascii<=102 and int(s[1])>=1 and int(s[1])<=6:  #verifie la validite des coordonnée
            return True
    elif partie["plateau"]["n"]==8 :
        if ascii>=97 and ascii<=104 and int(s[1])>=1 and int(s[1])<=8:  #verifie la validite des coordonnée
            return True
    return False
#17
from os import system

def effacer_terminal():
    #system('clear') #Linux
    system('cls')   #Windows

def tour_jeu(partie): #Place les pions sur le plateau en fonction des coordonées
    effacer_terminal()
    afficher_plateau2(partie["plateau"])
    if partie["joueur"]==1: #affiche le joueur qui doit jouer
        print("Joueur: N")
    elif partie["joueur"]==2:
        print("Joueur: B")
    print("tape: M  pour aller au menu principale")
    s=input("coordonée du pion a place ") #coordonée du pions à placer
    while s==len(s) :
        s=input("coordonée du pion a place ")
    if s=="M" or s=="m":
        return False
    if saisie_valide(partie,s):
        i=ord(s[0])-97          #convertie
        j=int(s[1])-1           #convertie
        mouvement(partie["plateau"],i,j,partie["joueur"]) #place le pion
        afficher_plateau2(partie["plateau"])
        return True
    return 0
#18
def saisir_action(partie):
    if partie is None:
        action=int(input("Taper 0 pour terminer le jeu, 1 pour commencer une nouvelle partie, 2 pour charger une partie\n"))
        while action!=0 and action != 1 and action !=2:
            action=int(input("Taper 0 pour terminer le jeu, 1 pour commencer une nouvelle partie, 2 pour charger une partie\n"))
        return action
    else:
        action=int(input("0 pour terminer le jeu, 1 pour commencer une nouvelle partie, 2 pour charger une partie, 3 pour sauvegarder une partie (si une partie est en cours), 4 pour reprendre la partie (si une partie est en cours).\n"))
        while action!=0 and action != 1 and action !=2 and action!=3 and action!=4:
            action=int(input("0 pour terminer le jeu, 1 pour commencer une nouvelle partie, 2 pour charger une partie, 3 pour sauvegarder une partie (si une partie est en cours), 4 pour reprendre la partie (si une partie est en cours).\n"))
        return action
#19
def jouer(partie):
    while not (fin_de_partie(partie["plateau"])):
        tab_save=partie["plateau"]["case"].copy() #copie de du tableau
        x=tour_jeu(partie)
        if x==False:
            return saisir_action(partie), partie
        while x == 0:
            x=tour_jeu(partie)
        if partie["plateau"]["case"] != tab_save:  #compareson avec l'ancien tableau
            adv=pion_adverse(partie["joueur"])  #joueur suivant
            if joueur_peut_jouer(partie["plateau"],adv): #test si on peut jouer
                partie["joueur"]=adv

    return True, partie
#20
def saisir_taille_plateau():
    n=int(input("Taille plateau (4,6 ou 8)"))
    while n!=4 and n!=6 and n!=8:
         n=int(input())
    return n
#21
from json import *
def sauvegarde_partie(partie):
    save=dumps(partie)  #formate
    f = open("sauvegarde_partie.json", "w") #ouvre le fichier
    f.write(save)   #ecrit dans le fichier
    f.close()   #ferme le fichier
    return True
#22
import os
def charge_partie():
    if os.path.exists("sauvegarde_partie.json"):
        print("le fichier est present")
        f=open("sauvegarde_partie.json", "r")
        read=f.read()
        f.close()
        p=loads(read)
        return p
    else:
        print("le fichier n'est pas present")
        return creer_partie(4)
#23
def othello():
    i=0
    while i>=0:
        a=saisir_action(None)
        if a == 0:
            return False
        elif a == 1:
            n=saisir_taille_plateau()
            p=creer_partie(n)
            b=jouer(p)
            if b[0]==3:
                sauvegarde_partie(b[1])
            elif b[0]==2:
                p=charge_partie()
                b=jouer(p)
                a==2
            elif b[0]==1:
                a=1
            elif b[0]==4:
                jouer(b[1])
            elif b[0]==0:
                return False
            elif b[0]==1:
                a=1
            elif b[0]==True:
                print(gagnant(b[1]["plateau"]))
        if a==2:
            p=charge_partie()
            b=jouer(p)
            if b[0]==3:
                sauvegarde_partie(b[1])
            elif b[0]==2:
                p=charge_partie()
                b=jouer(p)
                a==2
            elif b[0]==1:
                a=1
            elif b[0]==4:
                jouer(b[1])
            elif b[0]==0:
                return False
            elif b[0]==1:
                a=1
            elif b[0]==True:
                print(gagnant(b[1]["plateau"]))
        i+=1
#===================================Partie 4=======================================================
#Mode joueur contre ordinateur
def jouer_ordi(plateau, joueur):
    # Détermine les coups possibles pour l'ordinateur
    coups_possibles = coups_possibles_plateau(plateau, joueur)
    if not coups_possibles:
        return False

    # Détermine la valeur maximale pour chaque coup possible
    valeurs = []
    for coup in coups_possibles:
        copie_plateau = copie_plateau_othello(plateau)
        jouer_coup(copie_plateau, joueur, coup[0], coup[1])
        valeur = minimax(copie_plateau, pion_adverse(joueur), profondeur_max, True)
        valeurs.append(valeur)

    # Trouve l'indice du coup ayant la valeur maximale
    max_valeur = max(valeurs)
    indices = [i for i, v in enumerate(valeurs) if v == max_valeur]

    # Choisit un coup aléatoire parmi les coups ayant la valeur maximale
    index_choisi = random.choice(indices)
    coup_choisi = coups_possibles[index_choisi]

    # Joue le coup sur le plateau original
    jouer_coup(plateau, joueur, coup_choisi[0], coup_choisi[1])

    return True


othello()
