# =========================== #
# Initialise les bibliotèques #
# =========================== #

from tkinter import *
from tkinter.messagebox import *
import random, pygame

# =========================== #
#      Variables globale      #
# =========================== #

auteur = "Alexis Tan"
proba = [2,2,2,4] # 2 → 70% / 4 → 30%
tuiles = [ 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 ]
musique = [None, 'BGM-1.wav', 'BGM-2.wav', 'BGM-3.wav', 'BGM-4.wav']
couleurs = ['#FAF8EF', '#EDE0C8', '#EB9944', '#F59563', '#F67C5F', '#F65E3B', '#EDCF72', '#EDCC61', '#EDC850', '#EDC53F', '#F77D5F']

# =========================== #
#    Initialise les tuiles    #
# =========================== #

def Init(dim) :
    # Créer une grille non remplie
    X = dict()
    for i in range(dim) :
        X[i] = dict()
        for j in range(dim) :
            X[i][j] = 0

    # Ajoute aléatoirement une tuile 2 ou 4 sur la grille
    for i in range(3) : X[random.randint(0, dim-1)][random.randint(0, dim-1)] = random.choice(proba)

    return X

# =========================== #
#    Vérifie la fin du jeu    #
# =========================== #

def TestFin(grille) :

    # Condition 1 : Vérifie la présence de tuiles 2048 sur la grille
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if( grille[i][j] == 2048 ) :
                print("C'est gagné ! GG WP")
                return 1

    # Condition 0 : Vérifie la présence de tuiles 0 sur la grille
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if( grille[i][j] == 0 ) :
                return 0

    # Condition -1 : Si aucune case vide et aucun mouvement n'est possible

    # Si aucune des deux autres conditions est remplie, c'est perdu.
    print("C'est perdu ! ¯\_(ツ)_/¯")
    print("N'hésite pas à consulter ma page Règles.html pour avoir des astuces.")
    return -1

# =========================== #
#  Ajoute des tuile à la fin  #
# =========================== #

def AjoutTuile(grille) :
    # Vérifie la présence de tuiles 0 sur la grille et remplace par 0, 2 ou 4
    i = random.randint(0,3)
    j = random.randint(0,3)

    while(grille[i][j] != 0 ) :
        i = random.randint(0, len(grille)-1)
        j = random.randint(0, len(grille)-1)

    grille[i][j] = 2

    return grille

# =============================== #
#  Met à jour le score du joueur  #
# =============================== #

def ScoreJoueur(grille):
    sc = 0
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if( grille[i][j] in tuiles ) : sc += grille[i][j]

    return sc

# =========================== #
#   Lecture Droite → Gauche   #
# =========================== #

def Inverse(grille):
    buffer = []

    # Ajoute les listes au buffer
    for i in range(len(grille)):
        buffer.append([])
        # Ajoute les valeurs à la liste buffer[i]
        for j in range(len(grille[0])):
            buffer[i].append(grille[i][len(grille[0])-j-1])

    return buffer

# =========================== #
#   Lecture Droite → Gauche   #
# =========================== #

def GrilleTemp(Inverse):
    buffer = []

    # Ajoute les listes au buffer
    for i in range(len(Inverse[0])):
        buffer.append([])
        # Ajoute les valeurs à la liste buffer[i]
        for j in range(len(Inverse)):
            buffer[i].append(Inverse[j][i])

    return buffer

# =========================== #
#   Lecture Droite → Gauche   #
# =========================== #

def Remplace(Inverse):
    buffer = []
    finBoucle = False

    # Créer des listes temporaires
    for i in range(len(Inverse)):
        buffer.append([0] * len(Inverse))
        k = 0

        for j in range(len(Inverse)):
            if(Inverse[i][j] != 0):

                buffer[i][k] = Inverse[i][j]
                if( j != k ): finBoucle = True
                k += 1

    return (buffer, finBoucle)

# =========================== #
#     Addition des tuiles     #
# =========================== #

def Addition(Inverse):
    finBoucle = False
    for i in range(len(Inverse[0])):
        for j in range(len(Inverse[0])-1):
            if Inverse[i][j] == Inverse[i][j+1] and Inverse[i][j] != 0:
                # La tuile de droite est Additionnée à celle de gauche (on multiplie la tuile par 2)
                Inverse[i][j] *= 2
                # La tuile servant à l'Addition devient une case vide
                Inverse[i][j+1] = 0
                finBoucle = True
    return (Inverse, finBoucle)

# =========================== #
#        Déplacements         #
# =========================== #

def ActionHaut(grille) :
    print("[↑] Haut")
    # Lecture de haut en bas
    grille = GrilleTemp(grille)
    grille, finBoucle = Remplace(grille)
    # Addition des tuiles
    temp = Addition(grille)
    grille = temp[0]
    finBoucle = finBoucle or temp[1]
    # Lecture de gauche à droite
    grille = Remplace(grille)[0]
    grille = GrilleTemp(grille)
    return grille

def ActionBas(grille) :
    print("[↓] Bas")
    # Lecture de haut en bas
    grille = Inverse(GrilleTemp(grille))
    grille, finBoucle = Remplace(grille)
    # Addition des tuiles
    temp = Addition(grille)
    grille = temp[0]
    finBoucle = finBoucle or temp[1]
    # Lecture de droite à gauche
    grille = Remplace(grille)[0]
    grille = GrilleTemp(Inverse(grille))
    return grille

def ActionGauche(grille) :
    print("[←] Gauche")
    # Lecture de gauche à droite
    grille, finBoucle = Remplace(grille)
    # Addition des tuiles
    temp = Addition(grille)
    grille = temp[0]
    finBoucle = finBoucle or temp[1]
    # Lecture de gauche à droite
    grille = Remplace(grille)[0]
    return grille

def ActionDroite(grille) :
    print("[→] Droite")
    # Lecture de droite à gauche
    grille = Inverse(grille)
    grille, finBoucle = Remplace(grille)
    # Addition des tuiles
    temp = Addition(grille)
    grille = temp[0]
    finBoucle = finBoucle or temp[1]
    # Lecture de gauche à droite
    grille = Remplace(grille)[0]
    grille = Inverse(grille)

    return grille

# ================= #
# FONCTIONS DE MENU #
# ================= #

def About() : showinfo("A propos", "N'hésitez pas à visiter ma page de projet.\n\n- Alexis T.")

def Save() : showerror("Oups ¯\_(ツ)_/¯", "Je n'ai pas encore créer la fonction [Sauvegarder partie].")

def Load() : showerror("Oups ¯\_(ツ)_/¯", "Je n'ai pas encore créer la fonction [Charger partie].")

def Sound() : showerror("Oups ¯\_(ツ)_/¯", "Je n'ai pas encore créer la fonction [Volume].")

def Fullscreen() : showerror("Oups ¯\_(ツ)_/¯", "Je n'ai pas encore créer la fonction [Plein écran].")

# ======================== #
# Musique et effets sonore #
# ======================== #

def ChangerMusique(Son):
    i = int(Son)
    pygame.mixer.pause()
    pygame.mixer.init()
    BGM = pygame.mixer.Sound(musique[i])
    BGM.set_volume(.5)
    BGM.play(-1)

def SonWin():
    BGM = pygame.mixer.Sound("BGM-Win.wav")
    BGM.set_volume(1)
    BGM.play()

def SonLoose():
    pygame.mixer.init()
    BGM = pygame.mixer.Sound("BGM-Lose.wav")
    BGM.set_volume(1)
    BGM.play()
