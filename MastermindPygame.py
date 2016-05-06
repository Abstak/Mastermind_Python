#J'importe ma librairie pygame et des fonctions utiles
import pygame
from pygame.locals import *
from random import *
import time

#Variable de score que je mets hors de la boucle sinon il ne la trouve pas
s=0

#La boucle est infinie jusqu'a ce que restart=0
restart = 1
while restart:

#J'initialise les fonctions de pygame (je les active)
    pygame.init()

#Je fais des definitions pour lancer mes sons, ce sera bien plus court de les appeler comme ca
    def son_page():
        page=pygame.mixer.Sound("Musiques/son_page.wav")
        page.play()
    def son_fruit():
        effect=pygame.mixer.Sound("Musiques/son_fruit.wav")
        effect.play()
    def son_tada():
        effect=pygame.mixer.Sound("Musiques/son_tada.wav")
        effect.play()
    def son_dommage():
        effect=pygame.mixer.Sound("Musiques/son_dommage.wav")
        effect.play()
    def son_solution():
        son_solution=pygame.mixer.Sound("Musiques/son_solution.wav")
        son_solution.play()

    #J'initialise une variable qui compte le nombre de tours du joueurs (il y a 10 essais en tout)
    f=0

    def fin_de_la_partie():
        global f
        f=f+1

    #J'initialise les fonctions liees au son, a la musique
    pygame.mixer.init()

    #Je load la musique du jeu
    pygame.mixer.music.load("Musiques/musique_fond.wav")
    #Je choisis le parametre (-1) pour que la musique joue indefiniment
    pygame.mixer.music.play(-1)

    #Je cree ma fenetre de la taille de mes images
    fenetre = pygame.display.set_mode((600, 850), RESIZABLE)

    fond_frigo = pygame.image.load("Images/frigo.png")
    fenetre.blit(fond_frigo, (0,0))

    palette = pygame.image.load("Images/palette.png")
    #J'utilise une fonction pour litteralement "coller" l'image dans la fenetre aux cordonnees (408,440)
    fenetre.blit(palette, (408,440))

    intro_ratatouille_1 = pygame.image.load("Images/intro_ratatouille_1.png")
    fenetre.blit(intro_ratatouille_1, (0,0))

    #J'initialise des variables pour les coordonnees des boutons permettant de passer les pages
    bouton_x = 150
    bouton_y = 650
    bouton1 = pygame.image.load("Images/bouton1.png")
    fenetre.blit(bouton1, (bouton_x,bouton_y))

    #Je cree mon score
    #Je choisis la police du score, je choisit monospace en 15pt
    score=s
    scorefont=pygame.font.SysFont("monospace",15)
    scoretexte=scorefont.render("Ton score : " +str(score), 2, [255,160,122])
    fenetre.blit(scoretexte, (470,10))

    #Je rafraichis mon ecran
    pygame.display.flip()

    #Je cree une boucle pour l'intro du jeu
    intro = 2
    while intro:

        #J'ecoute les entrees sur mon ordinateur (la souris, le clavier...)
        for event in pygame.event.get():

            #On rappelle que event.pos[0] correspond aux abscisses et que event.pos[1] correspond aux ordonnees
            #Si on capte un evenement du type "mouvement de la souris" et qu'il est dans une zone precise (celle du bouton)
            if event.type == MOUSEMOTION and bouton_x<event.pos[0]<(bouton_x+70) and bouton_y<event.pos[1]<(bouton_y+70) :
                bouton2 = pygame.image.load("Images/bouton2.png")
                fenetre.blit(bouton2, (bouton_x,bouton_y))
                pygame.display.flip()
            if not event.type == MOUSEMOTION:
                fenetre.blit(bouton1, (bouton_x,bouton_y))
                pygame.display.flip()

            #Si un evenement du type "clique" et que c'est un clique gauche (1) et que...
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and bouton_x<event.pos[0]<(bouton_x+70) and bouton_y<event.pos[1]<(bouton_y+70):

                #J'appelle ma fonction pour jouer le son d'une page qui tourne
                son_page()
                if intro == 2:
                    aide_regles = pygame.image.load("Images/aide_regles.png")
                    fenetre.blit(aide_regles, (0,0))
                    pygame.display.flip()
                    intro = intro-1

                    #Je modifie la position de mon bouton pour tourner les pages, sinon j'ai des interactions genantes
                    bouton_x = 520
                    bouton_y = 770

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and bouton_x<event.pos[0]<(bouton_x+70) and bouton_y<event.pos[1]<(bouton_y+70) and intro == 1:
                son_page()
                fenetre.blit(fond_frigo, (0,0))
                fenetre.blit(palette, (408,440))
                pygame.display.flip()
                intro = 0

            #Petite ligne de code pour pouvoir quitter le jeu si on clique sur la croix rouge
            if event.type == QUIT :
                pygame.quit ()

    #Je prepare des variables globales que je mets hors de la boucle pour la position du fruit puis les pions de verification (oranges et verts)
    x=170
    y=600
    position_pion_verification_x=382
    position_pion_verification_y=608

    #Je cree de facon aleatoire une liste qui sera la combinaison de l'ordinateur
    combinaison_ordinateur=[randint(1,8) for z in range(1,5)]

    """
    Pour pouvoir tester le jeu comme il faut, ou pour s'aider tout simplement, on affiche la combinaison de l'ordinateur
    Tout en sachant que :
    1=pomme
    2=raisin
    3=banane
    4=cerise
    5=orange
    6=pasteque
    7=citron
    8=fraise
    """
    print (combinaison_ordinateur)

    #Je cree une seconde liste de 4 boites egalement que je remplis de 0 prealablement
    combinaison_joueur=[0 for u in range(1,5)]

    #Je cree une grande fonction jouer() pour pouvoir la repeter facilement
    def jouer ():

        #Je cree un compteur "joue"
        joue=0
        position_fruit_x=x      #Voila, nous utilisons les variables initialisees hors de la boucle
        position_fruit_y=y

        #Il y a 4 fruits dans une combinaison, le joueur joue donc 4 fois
        while joue<4:
            for event in pygame.event.get():

                """Il faut que je cree la combinaison du joueur selon sa demande
                Pour cela, il clique sur la palette de fruits
                En fonction de la position du clique, je place les fruits qu'il choisit et les ajoute a sa combinaison"""

                #Je m'occupe de la premiere colonne de fruits
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and 442<event.pos[0]<475:
                    son_fruit()
                    if 457<event.pos[1]<488:
                        pomme = pygame.image.load("Images/pomme.png")
                        fenetre.blit(pomme, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=1
                        joue=joue+1
                        pygame.display.flip()
                    if 503<event.pos[1]<530:
                        raisin = pygame.image.load("Images/raisin.png")
                        fenetre.blit(raisin, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=2
                        joue=joue+1
                        pygame.display.flip()
                    if 542<event.pos[1]<574:
                        banane = pygame.image.load("Images/banane.png")
                        fenetre.blit(banane, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=3
                        joue=joue+1
                        pygame.display.flip()
                    if 584<event.pos[1]<619:
                        cerise = pygame.image.load("Images/cerise.png")
                        fenetre.blit(cerise, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=4
                        joue=joue+1
                        pygame.display.flip()

                #Je m'occupe de la deuxieme colonne de fruits
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and 491<event.pos[0]<523:
                    son_fruit()
                    if 457<event.pos[1]<488:
                        orange = pygame.image.load("Images/orange.png")
                        fenetre.blit(orange, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=5
                        joue=joue+1
                        pygame.display.flip()
                    if 503<event.pos[1]<530:
                        pasteque = pygame.image.load("Images/pasteque.png")
                        fenetre.blit(pasteque, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=6
                        joue=joue+1
                        pygame.display.flip()
                    if 542<event.pos[1]<574:
                        citron = pygame.image.load("Images/citron.png")
                        fenetre.blit(citron, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=7
                        joue=joue+1
                        pygame.display.flip()
                    if 584<event.pos[1]<619:
                        fraise = pygame.image.load("Images/fraise.png")
                        fenetre.blit(fraise, (position_fruit_x,position_fruit_y))
                        position_fruit_x=position_fruit_x+50
                        combinaison_joueur[joue]=8
                        joue=joue+1
                        pygame.display.flip()
                if event.type == QUIT :
                    pygame.quit ()

        #Je dois maintenant verifier la combinaison du joueur et la comparer a celle de l'ordinateur, j'utilise un nouveau compteur
        verification=0

        xp=position_pion_verification_x
        yp=position_pion_verification_y

        while verification<4:
            #Je compare les boites des 2 listes
            if combinaison_joueur[verification]==combinaison_ordinateur[verification]:
                #Les pions noirs du mastermind traditionnel seront remplaces par des verts (= bon fruit et bien place)
                pion_vert = pygame.image.load("Images/pion_vert.png")
                fenetre.blit(pion_vert, (xp,yp)) #Pour ne pas donner d'indice, le pion ne sera pas mis a la premiere place
                pygame.display.flip()

                #Petit casse tete pour placer les pions de verification de facon a ce que le joueur ne sache pas (ou pas tout de suite en tout cas) a quel fruit ils correspondent
                if verification==0:
                    xp=xp-15
                    yp=yp+15
                if verification==1:
                    xp=xp+15
                if verification==2:
                    xp=xp-15
                    yp=yp-15
                verification=verification+1

            elif combinaison_joueur[verification]==combinaison_ordinateur[0] or combinaison_joueur[verification]==combinaison_ordinateur[1] or combinaison_joueur[verification]==combinaison_ordinateur[2] or combinaison_joueur[verification]==combinaison_ordinateur[3] and combinaison_joueur[verification]!=combinaison_ordinateur[verification]:
                #Les pions blancs du mastermind traditionnel seront remplaces par des oranges (= bon fruit mais mal place)
                rondb = pygame.image.load("Images/pion_orange.png") #Les pions blancs seront oranges (bon fruit mais mal place)
                fenetre.blit(rondb, (xp,(yp)))
                pygame.display.flip()
                if verification==0:
                    xp=xp-15
                    yp=yp+15
                if verification==1:
                    xp=xp+15
                if verification==2:
                    xp=xp-15
                    yp=yp-15
                verification=verification+1
            else:
                if verification==0:
                    xp=xp-15
                    yp=yp+15
                if verification==1:
                    xp=xp+15
                if verification==2:
                    xp=xp-15
                    yp=yp-15
                verification=verification+1

        #Si tout est bon, j'arrete la verification et le jeu
        if combinaison_joueur[0]==combinaison_ordinateur[0] and combinaison_joueur[1]==combinaison_ordinateur[1] and combinaison_joueur[2]==combinaison_ordinateur[2] and combinaison_joueur[3]==combinaison_ordinateur[3]:
            for u in range (0,10) :
                fin_de_la_partie()
        else :
            fin_de_la_partie()

    #Le joueur a droit a 10 essais
    while f<10 :
        jouer()
        #Je dois monter pour passer a la "ligne d'essai" suivante
        y=y-50
        position_pion_verification_y=position_pion_verification_y-50

    x_combinaison_ordinateur=155
    y_combinaison_ordinateur=70

    #Une fois fini, j'affiche en haut la solution de l'ordinateur, pour cela, une boucle for est utile
    for e in range (0,4):
        if combinaison_ordinateur[e]== 1:
            pomme = pygame.image.load("Images/pommeco.png")
            fenetre.blit(pomme, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50
        elif combinaison_ordinateur[e]== 2:
            raisin = pygame.image.load("Images/raisinco.png")
            fenetre.blit(raisin, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50
        elif combinaison_ordinateur[e]== 3:
            banane = pygame.image.load("Images/bananeco.png")
            fenetre.blit(banane, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50
        elif combinaison_ordinateur[e]== 4:
            cerise = pygame.image.load("Images/ceriseco.png")
            fenetre.blit(cerise, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50
        elif combinaison_ordinateur[e]== 5:
            orange = pygame.image.load("Images/orangeco.png")
            fenetre.blit(orange, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50
        elif combinaison_ordinateur[e]== 6:
            pasteque = pygame.image.load("Images/pastequeco.png")
            fenetre.blit(pasteque, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50
        elif combinaison_ordinateur[e]== 7:
            citron = pygame.image.load("Images/citronco.png")
            fenetre.blit(citron, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50
        elif combinaison_ordinateur[e]== 8:
            fraise = pygame.image.load("Images/fraiseco.png")
            fenetre.blit(fraise, (x_combinaison_ordinateur,y_combinaison_ordinateur))
            x_combinaison_ordinateur=x_combinaison_ordinateur+50

    son_solution()
    pygame.display.flip()

    #Je baisse un peu le son de fond pour que le changement ne soit pas brutal
    pygame.mixer.music.fadeout(2000)
    #Je fais patienter le programme 3 secondes pour que le joueur observe la solution
    time.sleep(3)

    #En fonction de si le joueur gagne ou perd, j'affiche un petit message accompagne d'une musique adequat, je modifie le score si besoin est
    if combinaison_joueur[0]==combinaison_ordinateur[0] and combinaison_joueur[1]==combinaison_ordinateur[1] and combinaison_joueur[2]==combinaison_ordinateur[2] and combinaison_joueur[3]==combinaison_ordinateur[3] :
        son_tada()
        gagne = pygame.image.load("Images/ratatouille_bravo.png")
        s=s+1
        fenetre.blit(gagne, (0,0))
    else:
        son_dommage()
        perdu = pygame.image.load("Images/ratatouille_perdu.png")
        fenetre.blit(perdu, (0,0))

    pygame.display.flip()

    #Cette derniere boucle permet de redemarer les programme en appuyant sur la touche entree
    redemarre=1
    while redemarre:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN :
                son_page()
                pygame.mixer.fadeout(1000)
                redemarre=redemarre-1
            if event.type == QUIT :
                pygame.quit ()
