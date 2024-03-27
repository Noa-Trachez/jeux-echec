import pygame as p
import moteurEchec

LARGEUR = HAUTEUR = 712 #La taille en pixel de notre fenêtre
Dimension = 8 #Le plato sera en 8x8
TailleCase= HAUTEUR // Dimension #La taille de notre case est égale a la hauteur en pixel divise par la dimension du plato
Max_IMGS = 15 #Pour les animations
IMAGES = {} #Variables qui va stocker toutes nos images de nos pions

#initialisation du logo et du nom du jeu
icon = p.image.load("NosImages/logo.jpg") #On charge l'image du logo
p.display.set_icon(icon) #on Initialise le logo dans pygame(p)
p.display.set_caption("Combat Royal") #On initialise le nom du jeux


def chargerLesImages():
    #Voici toutes les pieces dont on va avoir besoin dans notre jeux(sachant que certaines se repetent
    pieces = ["bTour", "bCavalier", "bFou", "bQueen", "bRoi", "bPion", "wTour", "wCavalier", "wFou", "wQueen", "wRoi", "wPion"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("NosImages/" + piece + ".png"), (TailleCase, TailleCase))
    #Ce for i in range va nous permettre d'acceder a
    # n'importe quelle image de notre dictionnaire grace a IMAGES['NomDeLaPiece']


def main():
    p.init() #On initialise pygame alias P
    ecran= p.display.set_mode((LARGEUR,HAUTEUR)) #On creer la fenetre avec nos variable créer precedement pour la definir
    temps=p.time.Clock() #On initialise une variable qui va recuperer le temps
    ecran.fill(p.Color("grey")) #On initialise un fond blanc
    sdj = moteurEchec.EtatDuJeu() #statut du jeu est recuperer dans notre module moteur echec et la fonction Etat Du Jeu
    DeplacementValide= sdj.ToutLesDeplacementsValide()
    mouvementEffectuer = False #Variable Drapeau quand un deplacement est effectuer
    chargerLesImages() #on charge nos images grace a la fonction definit ci-dessus
    jeuEnMarche = True #on initialise une variable qui tant qu'elle sera sur True le jeux fonctionnera
    caseSelectionner = ()
    # aucune case selectionner pour l'instant, cette variable vas enregistrer la dernière case selectionner sous forme de (tuple:  (ligne,collonne))
    clicJoueur = [] #La variable va garder les traces des deux derniers clcis sous forme de (deux tuples: en liste :[6,4); (4,4)])
    while jeuEnMarche: #Pour l'instant while True
        for e in p.event.get(): #on recupere les evenement tel que click fermeture de la fenetre qui se produise sur le pc
            if e.type == p.QUIT: #En l'occurence ici on ferme la fenetre
                jeuEnMarche = False #On retire le while True et on sors de la boucle
            elif e.type == p.MOUSEBUTTONDOWN :   #Quand bouton de souris pressé
                clicsouris = p.mouse.get_pos()  #(x, y) les coordonnées de x et y de la souris
                collone = clicsouris[0]//TailleCase #Coordonne de x divise par la taille de nos case(en division entiere)
                ligne = clicsouris[1]//TailleCase #Coordonne de y divise par la taille de nos case(en division entiere)
                if caseSelectionner == (ligne, collone): #Si l'utilisateur appuye deux fois sur la même case
                    caseSelectionner = () # deselectionne le pion
                    clicJoueur = [] # on retire la trace des deux derniere case selectionner
                else:
                    caseSelectionner = (ligne, collone) #On recupere les coordone de nos ligne et colone ci-dessus
                    clicJoueur.append(caseSelectionner) # apprendre l'ensemble des clic a ClicJoueur
                if len(clicJoueur) == 2: #après le deuxième clic
                    deplacement = moteurEchec.deplacement(clicJoueur[0], clicJoueur[1], sdj.board)
                    #on definit notre deplacement grace a notre module de moteur echec
                    print(deplacement.recuperLesNotationsOfficielles())
                    #On affiche le deplacement effectuer avec les notations officielles des echecs dans le shell
                    for i in range(len(DeplacementValide)):
                        if deplacement == DeplacementValide[i]:
                            sdj.faireDeplacement(DeplacementValide[i])
                            mouvementEffectuer = True
                        #Le statut du jeu va donc effectuer notre deplacement
                            caseSelectionner = () # la case selectionner est reinitialiser
                            clicJoueur = [] #Les Clic du joueur sont reinitialiser
                    if not mouvementEffectuer :
                        clicJoueur = [caseSelectionner]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    sdj.retourArriere()
                    mouvementEffectuer = True

            elif sdj.echecEtMate == True:
                if sdj.blancDeBouger == True :
                    print("Les noirs ont gagnés")
                else :
                    print("Les blancs ont gagnés")
                quit()
            elif sdj.matchNul == True:
                print("Match Nul")
                quit()
        if mouvementEffectuer :
            DeplacementValide = sdj.ToutLesDeplacementsValide()
            mouvementEffectuer = False


        dessinerEtatDuJeu(ecran,sdj, DeplacementValide, caseSelectionner) # On affiche  l'etat du jeu sur la taille de l'écran donné
        temps.tick(Max_IMGS) #Outils qui nous servira pour les animations
        p.display.flip() #On update notre ecran pour qu'il affiche les dernieres informations


'''
Previsualisation des mouvements
'''
def FluoCarre(ecran, sdj, DeplacementsValide, caseSelectionner):
    if caseSelectionner != ():
        l, c = caseSelectionner #ligne et colone prenne les valeurs correspondantes aux cases selectionné
        if sdj.board[l][c][0] == ('w' if sdj.blancDeBouger else 'b'): #la case selectionné appartient a une piece qui peux bouger
            #Fluoter la case selectionne
            s = p.Surface((TailleCase, TailleCase))
            s.set_alpha(150)#Valeur de la transparence 0 = transparent; 255 = opaque
            s.fill(p.Color('blue'))
            ecran.blit(s, (c*TailleCase, l*TailleCase))
            #Fluoter les mouvement de la case selectionner
            s.set_alpha(150)
            s.fill(p.Color(132, 210, 255))
            for deplacement in DeplacementsValide:
                if deplacement.ligneDepart == l and deplacement.colonneDepart ==c :
                    ecran.blit(s,(TailleCase*deplacement.colonneFin, TailleCase*deplacement.ligneFin))




def dessinerEtatDuJeu(ecran,sdj, DeplacementsValide, caseSelectionner): #raccourcis pour ecrire une unique fonction dans le while
    dessinerLePlato(ecran) #dessine les cases
    FluoCarre(ecran, sdj, DeplacementsValide, caseSelectionner)
    dessinerLesPieces(ecran, sdj.board)#affiche les pieces sur le plato

#On va dessiner les cases du plato
def dessinerLePlato(ecran):
    colors = [p.Color(186,213,107), p.Color("white")] # On initialise deux couleurs pour le fonds des cases du jeux
    for ligne in range(Dimension): #For ligne in range de 8 car plato de 8x8
        for colone in range(Dimension):#For colone in range de 8 car plato de 8x8
            colorDuCarre = colors[((ligne + colone) % 2)]
            # si le modulo est a 0 on applique la couleur colors[0] si il est a 1 on applique la colors[1]
            p.draw.rect(ecran,colorDuCarre,p.Rect(colone*TailleCase, ligne*TailleCase, TailleCase, TailleCase))
            #on dessine avec pygame un rectangle et on donne les parametres dont le module de pygame a besoin

#On va dessiner les piece sur plato
def dessinerLesPieces(ecran, plato):
    for ligne in range(Dimension): #For ligne in range de 8 car plato de 8x8
        for colone in range(Dimension): #For colone in range de 8 car plato de 8x8
            piece = plato[ligne][colone] #La piece correspond au tableau de notre module par rapport a la ligne et la colone
            if piece != "--": #Si il y a une piece en l'occurence on verifie si la piece est different du vide
                ecran.blit(IMAGES[piece], p.Rect(colone*TailleCase, ligne*TailleCase, TailleCase, TailleCase))
                #on affiche l'image SUR la case et pas dessous


if __name__ == "__main__":
    main()#on demarre le programme
    quit()#permet de quitter en appuyant sur l'ecran












