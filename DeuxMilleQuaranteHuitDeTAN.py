# =========================== #
# Initialise les bibliotèques #
# =========================== #

# Bibliothèques custom
from Fonction import *

# =========================== #
# Initialise la grille de jeu #
# =========================== #

def FENETRE(dim) :

    # =================================== #
    # Confirmation pour quitter la partie #
    # =================================== #
    def closeFenetre():
        verif = askquestion ("Quitter l'application", "Voulez vous vraiment quitter l'application ?")
        # Si l'user réponds oui
        if (verif == 'yes'):
            showwarning("(╯°□°）╯︵ 2048", "Ragequit c'est pas bien !")
            fenetre.destroy()
        # Si l'user réponds non
        else: showinfo("Quitter l'application", "¯\_(ツ)_/¯")

    # ============================== #
    # Fonctions qui gèrent le volume #
    # ============================== #
    def checkVolume(Valeur):
        # Actualisation du volume
        print("Volume de la musique : ", Valeur)

        Son = int(Valeur) / 100
        BGM.set_volume(Son)
        print(Son)

    def plus():
        Valeur.set(str(int(Valeur.get())+10))
        print("Volume de la musique augmenté à : ", Valeur.get())

        Son = Valeur.get() / 100
        BGM.set_volume(Son)
        print(Son)

    def moins():
        Valeur.set(str(int(Valeur.get())-10))
        print("Volume de la musique réduit à : ", Valeur.get())

        Son = Valeur.get() / 100
        BGM.set_volume(Son)
        print(Son)

    def lancer():
        BGM.set_volume(.5)

    def couper():
        BGM.set_volume(0)

    # ===================== #
    # Fonctions grille 2048 #
    # ===================== #
    def recupPartie() :
        dim = len(JEU)
        X = dict()
        for i in range(dim) :
            X[i] = dict()
            for j in range(dim) :
                try : X[i][j] = int(JEU[i][j].get())
                except : X[i][j] = 0
        return X

    def InjectionPartie(X) :
        for i in range(dim) :
            for j in range(dim) :
                try : (JEU[i][j]).set(X[i][j])
                except : (JEU[i][j]).set(0)
                if(int(JEU[i][j].get()) == 0) : (JEU[i][j]).set("")

    def Clavier(mouvement):
        # Event listener
        touche = mouvement.keysym

        # déplacement vers le haut
        if touche == 'Up':
            ActionHaut0()
            CMPT.set(CMPT.get()+1)
        # déplacement vers le bas
        if touche == 'Down':
            ActionBas0()
            CMPT.set(CMPT.get()+1)
        # déplacement vers la droite
        if touche == 'Right':
            ActionDroite0()
            CMPT.set(CMPT.get()+1)
        # déplacement vers la gauche
        if touche == 'Left':
            ActionGauche0()
            CMPT.set(CMPT.get()+1)

        # =============== #
        # KeyEvent custom #
        # =============== #

        # Nouvelle partie → keybind [N]
        if touche == 'n' or touche == 'N' : ActionRecommencer()
        # Sauvegarder → keybind [S]
        if touche == 's' or touche == 'S' : Save()
        # Charger partie → keybind [L]
        if touche == 'l' or touche == 'L' : Load()
        # Charger partie → keybind [Y]
        if touche == 'y' or touche == 'Y' : Sound()
        # Charger partie → keybind [F]
        if touche == 'f' or touche == 'F' : Fullscreen()
        # Fermer fenetre → keybind [+]
        if touche == 'plus' : plus()
        # Fermer fenetre → keybind [-]
        if touche == 'minus' : moins()
        # Fermer fenetre → keybind [/]
        if touche == 'slash' : couper()
        # Fermer fenetre → keybind [X]
        if touche == 'x' or touche == 'X' : closeFenetre()

        # Execute un son secret
        if touche == 'p' : SecretSound()

    def ActionRecommencer() :
        X=Init(dim)
        for i in range(dim) :
            for j in range(dim) :
                (JEU[i][j]).set(X[i][j])
                if(X[i][j] == 0 ) : (JEU[i][j]).set("")
        CMPT.set(0)
        SCORE.set(0)

    def ActionHaut0() :
        InjectionPartie(ActionHaut(recupPartie()))
        InjectionPartie(AjoutTuile(recupPartie()))
        TestFin0(recupPartie())

    def ActionBas0() :
        InjectionPartie(ActionBas(recupPartie()))
        InjectionPartie(AjoutTuile(recupPartie()))
        TestFin0(recupPartie())

    def ActionGauche0() :
        InjectionPartie(ActionGauche(recupPartie()))
        InjectionPartie(AjoutTuile(recupPartie()))
        TestFin0(recupPartie())

    def ActionDroite0() :
        InjectionPartie(ActionDroite(recupPartie()))
        InjectionPartie(AjoutTuile(recupPartie()))
        TestFin0(recupPartie())

    def TestFin0(X) :
        SCORE.set(ScoreJoueur(X))
        if(HIGHSCORE.get() <= SCORE.get()) : HIGHSCORE.set(SCORE.get())
        test=TestFin(X)
        if(test == 1 ) :
            SonWin()
            showinfo("FIN DE PARTIE", "Bravo ! Vous avez gagné en "+str(CMPT.get())+" coups. Recommencer ?")
        if(test == -1 ) :
            SonLoose()
            showinfo("FIN DE PARTIE", "Perdu ! Il vous a fallu "+str(CMPT.get())+" coups pour perdre... comment dire. On s'arrête là ou on recommence ?")
        if(test != 0 ) : ActionRecommencer()

    fenetre = Tk()
    fenetre.title('2048 par ' + auteur)

    # ================ #
    # Variables de jeu #
    # ================ #

    # Compteur
    CMPT=IntVar()
    CMPT.set(0)

    # Score du joueur
    SCORE = IntVar()
    SCORE.set(0)

    # Meilleur score de la session
    HIGHSCORE = IntVar()
    HIGHSCORE.set(SCORE.get())

    # Gère la variable son
    Valeur = IntVar()
    Valeur.set(50)

    # Compteur
    SECONDS=IntVar()
    SECONDS.set(0)

    # S'occupe de changer la musique
    Son = IntVar()
    Son.set(0)

    # =============================================================== #
    # Parcours la grille tour 0 et remplace les 0 par des cases vides #
    # =============================================================== #
    X = Init(dim)
    JEU = dict()
    for i in range(dim) :
        JEU[i] = dict()
        for j in range(dim) :
            JEU[i][j] = StringVar()
            (JEU[i][j]).set(X[i][j])
            if(X[i][j] == 0 ) : (JEU[i][j]).set("")

    base = 80 # Taille en px d'un carré
    if(dim>7) : base = 50
    marge = 10 # Marge de beauté

    hauteur = dim * base + 2 * marge + 150
    largeur = dim * base + 2 * marge + 150

     # Largeur et hauteur minimum de l'application
    fenetre.minsize(largeur, hauteur)
    canvas = Canvas(fenetre, background="#fae3d9", width=largeur, height=hauteur )

    # ================= #
    c_fg='black'
    c_bg ='#fae3d9'

    case = dict()
    for i in range(dim) :
        case[i] = dict()
        for j in range(dim) :
            canvas.create_rectangle( (base*i+marge,base*j+marge), (base*(i+1)+marge,base*(j+1)+marge), width=1, fill="#fae3d9")

            if  ((JEU[i][j]).get() == 0 ) : c_fg='white'

            # Changement de la couleur des tuiles ( WIP )
            elif((JEU[i][j]).get() == 2 ) : c_fg='#FAF8EF'
            elif((JEU[i][j]).get() == 4 ) : c_fg='#EDE0C8'
            elif((JEU[i][j]).get() == 8 ) : c_fg='#EB9944'
            elif((JEU[i][j]).get() == 16 ) : c_bg='#F59563'
            elif((JEU[i][j]).get() == 32 ) : c_bg='#F67C5F'
            elif((JEU[i][j]).get() == 64 ) : c_bg='#F65E3B'

            L = Label(fenetre, textvariable = JEU[i][j], fg=c_fg, bg=c_bg)
            L.place( x = base * j + base // 2, y = base * i + base // 2, anchor="nw")
            #L.config( font = ("Courier", 10, 'bold') )

    # ==================== #
    # Gère le score du jeu #
    # ==================== #
    highscore = "Meilleur score : "
    L=Label(fenetre, text= highscore, fg = 'black', bg=c_bg)
    L.place(x=largeur-marge-140, y = 30, anchor="sw")

    L=Label(fenetre, textvariable= HIGHSCORE, fg='black', bg=c_bg)
    L.place(x=largeur-marge-140+len(highscore)*5, y = 30, anchor="sw")

    # ==================== #
    # Gère le score du jeu #
    # ==================== #
    score = "Score : "
    L=Label(fenetre, text=score, fg='black', bg=c_bg)
    L.place(x=largeur-marge-140, y = 50, anchor="sw")

    L=Label(fenetre, textvariable=SCORE, fg='black', bg=c_bg)
    L.place(x=largeur-marge-140+len(score)*5, y = 50, anchor="sw")

    # ============================= #
    # Gère le nombre de déplacement #
    # ============================= #
    txt = "Nb. de mouvements : "
    L=Label(fenetre, text=txt, fg='black', bg=c_bg)
    L.place(x=largeur-marge-140, y = 70, anchor="sw")

    L=Label(fenetre, textvariable=CMPT, fg='black', bg=c_bg)
    L.place(x=largeur-marge-140+len(txt)*6, y = 70, anchor="sw")

    # ============================= #
    # Gère le nombre de déplacement #
    # ============================= #
    sec = "Temps écoulé : "
    L=Label(fenetre, text=sec, fg='black', bg=c_bg)
    L.place(x=largeur-marge-140, y = 90, anchor="sw")

    L=Label(fenetre, textvariable=SECONDS, fg='black', bg=c_bg)
    L.place(x=largeur-marge-140+len(sec)*6, y = 90, anchor="sw")

    # ============================== #
    # Gère les boutons de la fenetre #
    # ============================== #

    # Création du bouton Recommencer
    BoutonNewP = Button(fenetre, text ='Nouvelle Partie [N]', command = ActionRecommencer)
    BoutonNewP.place(x=marge, y = hauteur-120 , width=120, height=30, anchor="sw")
    # Création du bouton Sauvegarder
    BoutonSave = Button(fenetre, text ='Sauver Partie [S]', command=Save)
    BoutonSave.place(x=marge, y = hauteur-80 , width=120, height=30, anchor="sw")
    # Création du bouton Charger
    BoutonLoad = Button(fenetre, text ='Charger Partie [L]', command=Load)
    BoutonLoad.place(x=marge, y = hauteur-50, width=120, anchor="sw")
    BoutonLoad.config (state = DISABLED)
    # Création du bouton Quitter
    BoutonQuitter = Button(fenetre, text ='Quitter [X]', command = closeFenetre)
    BoutonQuitter.place(x=marge, y = hauteur-10, width=120, anchor="sw")

    # Création d'un widget Button (bouton -)
    BtnVolNone = Button(fenetre, text = "Couper la musique [/]", command=couper)
    BtnVolNone.place(x = largeur-marge, y = hauteur-120, width=340, height=30, anchor="se")
    # Création du widget volume
    Volume = Scale(fenetre, from_ = 0 , to = 100, resolution = 1, orient = HORIZONTAL, width = 5, label="Volume de la musique (BGM)", variable = Valeur, command = checkVolume)
    Volume.place(x = largeur-marge-25, y = hauteur-65, width=290, height=50, anchor="se")
    # Création d'un widget Button (bouton +)
    BtnVolPlus = Button(fenetre, text = "[+]", relief=FLAT, command=plus)
    BtnVolPlus.place(x = largeur-marge, y = hauteur-65, width=25, height=50, anchor="se")
    # Création d'un widget Button (bouton -)
    BtnvolMoin = Button(fenetre, text = "[-]", relief=FLAT, command=moins)
    BtnvolMoin.place(x = largeur-marge-315, y = hauteur-65, width=25, height=50, anchor="se")

    # Création d'un widget Scale ( changement de BGM )
    changeBGM = Scale(fenetre, from_ = 1 , to = 4, orient = HORIZONTAL, width = 5, label = "Change la musique du jeu (BGM)", tickinterval = 1, showvalue=0, variable = Son, command = ChangerMusique)
    changeBGM.place(x = largeur-marge, y = hauteur-10, width=340, height=50, anchor="se")

    # ========================== #
    # Gère le menu de la fenetre #
    # ========================== #
    menu = Menu(fenetre)
    fenetre.configure(menu = menu, width=200)

    # ========================= #
    # Créer les onglets de menu #
    # ========================= #
    jeu = Menu(menu, tearoff=0)
    options = Menu(menu, tearoff=0)
    apropos = Menu(menu, tearoff=0)

    # ======================================= #
    # Ajoute les onglets sur la barre de menu #
    # ======================================= #
    menu.add_cascade(label = "Jeu", menu = jeu)
    menu.add_cascade(label = "Options", menu = options)
    menu.add_cascade(label = "A propos", menu = apropos)

    # ====================================== #
    # Ajoute les commandes de l'onglet [Jeu] #
    # ====================================== #
    jeu.add_command(label = "[N] - Nouvelle partie", command = ActionRecommencer)
    jeu.add_command(label = "[S] - Sauvegarder la partie", command = Save)
    jeu.add_command(label = "[L] - Charger une partie", command =  Load)
    jeu.add_command(label = "[X] - Quitter le jeu", command = closeFenetre)

    # ========================================== #
    # Ajoute les commandes de l'onglet [Options] #
    # ========================================== #
    options.add_command(label = "[+] - Augmenter le volume", command = plus)
    options.add_command(label = "[-] - Diminuer le volume", command = moins)
    options.add_command(label = "[/] - Couper la musique", command = couper)

    options.add_command(label = "[F] - Plein écran", command = Fullscreen)

    # =========================================== #
    # Ajoute les commandes de l'onglet [A propos] #
    # =========================================== #
    apropos.add_command(label = "A propos", command = About)

    # ============================ #
    # Gère la taille de la fenetre #
    # ============================ #
    fenetre.geometry(str(largeur)+"x"+str(hauteur))

    # ============================== #
    # S'occupe de la musique de fond #
    # ============================== #
    pygame.mixer.init()
    BGM = pygame.mixer.Sound("BGM-1.wav")
    BGM.set_volume(.5)
    BGM.play(-1)

    # ====================================== #
    # Permet le fonctionnement des keyevents #
    # ====================================== #
    canvas.focus_set()
    canvas.bind('<Key>', Clavier)

    canvas.grid()
    fenetre.mainloop()

# Dimension du 2048 - usuellement 4
dim = 0

# J'ai modifié légèrement les conditions pour avoir strictement entre 3 et 10 en entrée
while( dim <= 2 or dim >= 11) :
    try : dim = int(input("Quelle taille votre 2048 (entre 3 et 10): "))
    except : dim = 0

#Fonction principale
FENETRE(dim)
