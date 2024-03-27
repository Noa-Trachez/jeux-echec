class EtatDuJeu():
    def __init__(self):
        #Le plato est tableau de 8x8, chaque element de notre tableau a 1caractère qui definit sa couleur
        # 'b' ou 'w' pour 'black' ou 'white' et ce qui le precede la piece a laquelle cela correspond
        # les "--" representent les cases vide
        self.board =[
            ["bTour", "bCavalier", "bFou", "bQueen", "bRoi", "bFou", "bCavalier", "bTour"],
            ["bPion", "bPion", "bPion", "bPion", "bPion", "bPion", "bPion", "bPion"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wPion", "wPion", "wPion", "wPion", "wPion", "wPion", "wPion", "wPion"],
            ["wTour", "wCavalier", "wFou", "wQueen", "wRoi", "wFou", "wCavalier", "wTour"]]
        self.fonctionMouvement = {'P': self.recupererMouvementPion, 'T': self.recupererMouvementTour,
                                'C': self.recupererMouvementCavalier, 'F': self.recupererMouvementFou,
                                'Q': self.recupererMouvementQueen, 'R': self.recupererMouvementRoi}
        self.blancDeBouger = True #Une variable qui donne le tour soit au noir soit au blanc
        self.repertoireMouvement = [] #Une variable qui va stocker tout nos mouvement pour pouvoir revenir en arriere
        self.EmplacementRoiBlanc = (7, 4)
        self.EmplacementRoiNoir = (0, 4)
        self.echecEtMate = False
        self.matchNul = False
        self.enpassantPossible = () #Coordonnée du carré ou la prise en passant est possible
        self.RockPossible = RockValide(True, True, True, True)
        self.RockLog = [RockValide(self.RockPossible.wrc, self.RockPossible.brc, self.RockPossible.wqc, self.RockPossible.bqc)]

    def faireDeplacement(self, deplacement):
        self.board[deplacement.ligneDepart][deplacement.colonneDepart] = "--"
        #La case de depart de notre pion est remplace par une case vide
        self.board[deplacement.ligneFin][deplacement.colonneFin] = deplacement.pieceDeplacer
        #La case d'arriver est remplacer par notre pion dans le board
        self.repertoireMouvement.append(deplacement) #enregistre le deplacement pour pouvoir revenir sur un ancien coup
        self.blancDeBouger = not self.blancDeBouger #changer le tour de jeux des joueurs
        #Mettre a jour l'emplacement du Roi si il est bouger
        if deplacement.pieceDeplacer == "wRoi" :
            self.EmplacementRoiBlanc = (deplacement.ligneFin, deplacement.colonneFin)
        elif deplacement.pieceDeplacer == "bRoi" :
            self.EmplacementRoiNoir = (deplacement.ligneFin, deplacement.colonneFin)
        #Promotion du pion
        if deplacement.PromotionPion:
            self.board[deplacement.ligneFin][deplacement.colonneFin] = deplacement.pieceDeplacer[0] + 'Queen'
        #Prise en passant
        if deplacement.estEnpassantDeplacement:
            self.board[deplacement.ligneDepart][deplacement.colonneFin] = '--' #capture le pion
        #Update de la possibilité de la prise en passant
        if deplacement.pieceDeplacer[1] == "P" and abs(deplacement.ligneDepart - deplacement.ligneFin) == 2: #Seulement si il a avancé de deux cases
            #Abs => valeur absolue (positive)
            self.enpassantPossible = ((deplacement.ligneDepart + deplacement.ligneFin)//2, deplacement.colonneDepart)
        else:
            self.enpassantPossible =()
        if deplacement.estRock:
            if deplacement.colonneFin - deplacement.colonneDepart == 2: #Rock du cote Roi
                self.board[deplacement.ligneFin][deplacement.colonneFin-1] = self.board[deplacement.ligneFin][deplacement.colonneFin+1]#deplace la tour
                self.board[deplacement.ligneFin][deplacement.colonneFin+1] = '--' #on efface la tour
            else : #Rock cote Queen
                self.board[deplacement.ligneFin][deplacement.colonneFin + 1] = self.board[deplacement.ligneFin][deplacement.colonneFin-2]#deplace la tour
                self.board[deplacement.ligneFin][deplacement.colonneFin-2] = '--' #on efface la tour

        #Update le Rock - changement de place Tour Roi
        self.updateRockPossible(deplacement)
        self.RockLog.append(RockValide(self.RockPossible.wrc, self.RockPossible.brc, self.RockPossible.wqc, self.RockPossible.bqc))



    def retourArriere(self):
        if len(self.repertoireMouvement) != 0:#On s'assure que au moins un deplacement a ete effectue
            deplacement = self.repertoireMouvement.pop()
            # On recupere le dernier deplacement enregistrer dans le repertoire des mouvements
            self.board[deplacement.ligneDepart][deplacement.colonneDepart] = deplacement.pieceDeplacer
            #On remet la piece deplacer a sa place
            self.board[deplacement.ligneFin][deplacement.colonneFin] = deplacement.pieceManger
            #On replace la piece manger donc soit le '--' soit le pion
            self.blancDeBouger = not self.blancDeBouger #Permettre de remettre le bon tour
            # Mettre a jour l'emplacement du Roi si besoin
            if deplacement.pieceDeplacer == "wRoi":
                self.EmplacementRoiBlanc = (deplacement.ligneDepart, deplacement.colonneDepart)
            elif deplacement.pieceDeplacer == "bRoi":
                self.EmplacementRoiNoir = (deplacement.ligneDepart, deplacement.colonneDepart)

            #Undo la prise en passant
            if deplacement.estEnpassantDeplacement:
                self.board[deplacement.ligneFin][deplacement.colonneFin] = '--' #quitte le carré vide
                self.board[deplacement.ligneDepart][deplacement.colonneFin] = deplacement.pieceManger
                self.enpassantPossible = (deplacement.ligneFin, deplacement.colonneFin)

            #Undo l'avancement de deux cases
            if deplacement.pieceDeplacer[1] == "P" and abs(deplacement.ligneDepart - deplacement.ligneFin) == 2:
                self.enpassantPossible = ()

            #Undo Possibilite de Rock
            self.RockLog.pop() #on retire les derniere modification du droit de rock
            nouveauDroit = self.RockLog[-1]
            self.RockPossible = RockValide(nouveauDroit.wrc, nouveauDroit.brc, nouveauDroit.wqc, nouveauDroit.bqc)

            #Undo le rock
            if deplacement.estRock:
                if deplacement.colonneFin - deplacement.colonneDepart ==2: #CoteRoi
                    self.board[deplacement.ligneFin][deplacement.colonneFin + 1] = self.board[deplacement.ligneFin][deplacement.colonneFin - 1]
                    self.board[deplacement.ligneFin][deplacement.colonneFin - 1] = '--'
                else : #CoteReine
                    self.board[deplacement.ligneFin][deplacement.colonneFin - 2] = self.board[deplacement.ligneFin][deplacement.colonneFin + 1]
                    self.board[deplacement.ligneFin][deplacement.colonneFin + 1] = '--'



    ###Update la possibilite de rock
    def updateRockPossible(self, deplacement):
        if deplacement.pieceDeplacer == 'wRoi':
            self.RockPossible.wrc = False
            self.RockPossible.wqc = False
        elif deplacement.pieceDeplacer == 'bRoi':
            self.RockPossible.bqc = False
            self.RockPossible.brc = False
        elif deplacement.pieceDeplacer == "wTour":
            if deplacement.colonneDepart == 0: #Tour de gauche
                self.RockPossible.wqc = False
            elif deplacement.colonneDepart == 7: #Tour de droite
                self.RockPossible.wrc = False
        elif deplacement.pieceDeplacer == "bTour":
            if deplacement.colonneDepart == 0: #Tour de gauche
                self.RockPossible.bqc = False
            elif deplacement.colonneDepart == 7: #Tour de droite
                self.RockPossible.brc = False




    def ToutLesDeplacementsValide (self) :
        tempEnPassantPossible = self.enpassantPossible
        tempRockPossible = RockValide(self.RockPossible.wrc, self.RockPossible.brc, self.RockPossible.wqc, self.RockPossible.bqc)
        #1) Generer tout les déplacements possibles
        moves = self.ToutLesDeplacementsPossible()
        if self.blancDeBouger:
            self.recupererRock(self.EmplacementRoiBlanc[0], self.EmplacementRoiBlanc[1], moves)
        else :
            self.recupererRock(self.EmplacementRoiNoir[0], self.EmplacementRoiNoir[1], moves)
        #2) pour chaque déplacement, les faires
        for i in range(len(moves)-1, -1, -1): #Pour supprimer un element d'une liste en la lisant à l'envers pour eviter des bugs
            self.faireDeplacement(moves[i])
            #3) générer tout les deplacement des adversaires
            #4) pour chaques adversaire, voire si il attaque votre Roi
            self.blancDeBouger = not self.blancDeBouger
            if self.EnEchec():
                moves.remove(moves[i]) #5) Si l'adversaire attaque votre roi, le déplacement n'est pas valide
            self.blancDeBouger = not self.blancDeBouger
            self.retourArriere()
        if len(moves) == 0: # Si il n'y a plus auncun déplacement possible
            if self.EnEchec():
                self.echecEtMate = True #On est soit en echec et math
            else:
                self.matchNul = True # Ou soit en match nul
        else:
            self.echecEtMate = False #Si des deplacement sont encore disponible, on est ni l'un ni l'autre
            self.matchNul = False #Si des deplacement sont encore disponible, on est ni l'un ni l'autre
        self.enpassantPossible = tempEnPassantPossible
        self.RockPossible = tempRockPossible
        return moves

    '''
    Determine si le joueur actuel est en echec
    '''
    def EnEchec(self):
        if self.blancDeBouger:
            return self.CarreAttaquer(self.EmplacementRoiBlanc[0], self.EmplacementRoiBlanc[1])
        else:
            return self.CarreAttaquer(self.EmplacementRoiNoir[0], self.EmplacementRoiNoir[1])
    '''
    Determine si l'adversaire peut attaquer le carrer l, c
    '''
    def CarreAttaquer(self, l, c):
        self.blancDeBouger = not self.blancDeBouger #changer pour le tour de l'adversaire
        deplacementAdversaire = self.ToutLesDeplacementsPossible()
        self.blancDeBouger = not self.blancDeBouger
        for deplacement in deplacementAdversaire:
            if deplacement.ligneFin == l and deplacement.colonneFin == c: #le carrer est attaquer
                return True
        return False



    def ToutLesDeplacementsPossible (self) :
        Deplacements = []
        for ligne in range (len(self.board)): #Nombre de ligne
            for colone in range(len(self.board[ligne])): #Nombre de colone dans la ligne
                COULEURaJouer = self.board[ligne][colone][0]
                #Donne la premiere lettre du pion dans le tableau soit 'w'/'b'/'-'
                if (COULEURaJouer == "w" and self.blancDeBouger == True) or (COULEURaJouer == "b" and not self.blancDeBouger):
                    piece = self.board[ligne][colone][1]
                    #Donne la Deuxieme lettre du pion soit 'R'/'Q'/'P'/'-'/'C'/'T'/'F'
                    self.fonctionMouvement[piece](ligne, colone, Deplacements)
        return Deplacements


#Mouvement de maniere simple et naïve plus facile a coder pour nous
    def recupererMouvementPion(self, l, c, Deplacements):
        if self.blancDeBouger: #Au tour du pion blanc
            if self.board[l-1][c] == "--": #Pion avance de 1 case
                Deplacements.append(deplacement((l,c), (l-1,c), self.board))
                if l == 6 and self.board[l-2][c] == "--": #Pion avance de 2 case si il n'a pas encore bouger
                    Deplacements.append(deplacement((l,c),(l-2,c),self.board))
            if c-1 >=0 : #Possibilite de capture sur la diagonale gauche
                if self.board[l-1][c-1][0] == 'b':#Si ennemi sur la diagonale gauche
                    Deplacements.append(deplacement((l,c),(l-1,c-1), self.board))
                elif (l-1, c-1) == self.enpassantPossible:
                    Deplacements.append(deplacement((l, c), (l - 1, c - 1), self.board, estEnpassantPossible=True))

            if c+1 <= 7: #Possibilite de capture sur la diagonale droite
                if self.board[l-1][c+1][0] == 'b' :#Si ennemi sur la diagonale droite
                    Deplacements.append(deplacement((l,c),(l-1,c+1),self.board))
                elif (l - 1, c + 1) == self.enpassantPossible:
                    Deplacements.append(deplacement((l, c), (l - 1, c + 1), self.board, estEnpassantPossible=True))
        else : #Au tour du pion Noir
            if self.board[l+1][c] == "--": #Pion avance de 1 case
                Deplacements.append(deplacement((l,c), (l+1,c), self.board))
                if l == 1 and self.board[l+2][c] == "--": #Pion avance de 2 case si il n'a pas encore bouger
                    Deplacements.append(deplacement((l,c),(l+2,c),self.board))
            if c-1 >=0 : #Possibilite de capture sur la diagonale gauche
                if self.board[l+1][c-1][0] == 'w':#Si ennemi sur la diagonale gauche
                    Deplacements.append(deplacement((l,c),(l+1,c-1), self.board))
                elif (l + 1, c - 1) == self.enpassantPossible:
                    Deplacements.append(deplacement((l, c), (l + 1, c - 1), self.board, estEnpassantPossible=True))
            if c+1 <= 7: #Possibilite de capture sur la diagonale droite
                if self.board[l+1][c+1][0] == 'w' :#Si ennemi sur la diagonale droite
                    Deplacements.append(deplacement((l,c),(l+1,c+1),self.board))
                elif (l + 1, c + 1) == self.enpassantPossible:
                    Deplacements.append(deplacement((l, c), (l + 1, c + 1), self.board, estEnpassantPossible=True))
        #Ajouter la promotion du pion lorsqu'il arrive a la derniere ligne du tableau



    def recupererMouvementTour(self, l, c, Deplacements):
        directionTour = ((-1,0),(0,-1),(1,0),(0,1))#haut gauche bas droite
        if self.blancDeBouger:
            CouleurEnnemi = "b"
        else :
            CouleurEnnemi = "w"
        for d in directionTour:
            for i in range (1,8): #Elle peut faire au maximum 7 cases
                ligneFin = l + d[0]*i
                coloneFin = c + d[1]*i
                if 0<= ligneFin < 8 and 0<= coloneFin <8 : #Sur le tableau de nos données
                    dernierePiece = self.board[ligneFin][coloneFin]
                    if dernierePiece == "--":#case vide
                        Deplacements.append(deplacement((l,c),(ligneFin,coloneFin),self.board))
                    elif dernierePiece[0] == CouleurEnnemi:
                        #La piece ciblé est ennemi (dernierePiece[0] renvoie 'b' ou 'w')
                        Deplacements.append(deplacement((l,c),(ligneFin,coloneFin),self.board))
                        break
                    else: #Piece Allié
                        break
                else: #en dehors du plato
                    break


    def recupererMouvementFou(self, l, c, Deplacements):
        directionFou = ((-1, -1),(-1,1),(1,-1),(1,1)) #Toutes les diagonales
        couleurEnnemi = "b" if self.blancDeBouger else "w"
        for d in directionFou:
            for i in range (1,8): #Elle peut faire au maximum 7 cases
                ligneFin = l + d[0] * i
                coloneFin = c + d[1] * i
                if 0<= ligneFin < 8 and 0<= coloneFin <8 : #Sur le plato
                    dernierePiece = self.board[ligneFin][coloneFin]
                    if dernierePiece == "--":#case vide
                        Deplacements.append(deplacement((l,c),(ligneFin,coloneFin),self.board))
                    elif dernierePiece[0] == couleurEnnemi:
                        #La piece ciblé est ennemi (dernierePiece[0] renvoie 'b' ou 'w')
                        Deplacements.append(deplacement((l,c),(ligneFin,coloneFin),self.board))
                        break
                    else: #Piece Allié
                        break
                else: #en dehors du plato
                    break

    def recupererMouvementCavalier(self, l, c, Deplacements):
        DeplacementCavalier= ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        CouleurAllier = "w" if self.blancDeBouger else "b"
        for d in DeplacementCavalier:
            ligneFin = l + d[0]
            coloneFin = c + d[1]
            if 0 <= ligneFin < 8 and 0 <= coloneFin < 8:  # Sur le plato
                dernierePiece = self.board[ligneFin][coloneFin]
                if dernierePiece[0] != CouleurAllier:
                        #La piece ciblé est ennemi (dernierePiece[0] renvoie 'b' ou 'w')
                        Deplacements.append(deplacement((l,c),(ligneFin,coloneFin),self.board))

    def recupererMouvementQueen(self, l, c, Deplacements):
        self.recupererMouvementTour(l, c, Deplacements)
        self.recupererMouvementFou(l, c, Deplacements)

    def recupererMouvementRoi(self, l, c, Deplacements):
        deplacementRoi = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        CouleurAllier = "w" if self.blancDeBouger else "b"
        for i in range (8):
            ligneFin = l + deplacementRoi[i][0]
            coloneFin = c + deplacementRoi[i][1]
            if 0 <= ligneFin < 8 and 0 <= coloneFin < 8:  # Sur le plato
                dernierePiece = self.board[ligneFin][coloneFin]
                if dernierePiece[0] != CouleurAllier:
                        #La piece ciblé est ennemi (dernierePiece[0] renvoie 'b' ou 'w')
                        Deplacements.append(deplacement((l,c),(ligneFin,coloneFin),self.board))


        '''
        Generer tout les rock possible
        '''
    def recupererRock(self, l, c, Deplacements):
        if self.CarreAttaquer(l, c):
            return #impossible de Rock en echec
        if (self.blancDeBouger and self.RockPossible.wrc) or (not self.blancDeBouger and self.RockPossible.brc):
            self.recupererRoiCoteRock(l,c,Deplacements)
        if (self.blancDeBouger and self.RockPossible.wqc) or (not self.blancDeBouger and self.RockPossible.bqc):
            self.recupererQueenCoteRock(l, c, Deplacements)

    def recupererRoiCoteRock(self, l, c, Deplacements):
        if self.board[l][c+1] == '--' and self.board[l][c+2] == '--':
            if not self.CarreAttaquer(l,c+1) and not self.CarreAttaquer(l, c+2):
                Deplacements.append(deplacement((l,c),(l,c+2), self.board, estRock=True))


    def recupererQueenCoteRock(self, l, c, Deplacements):
        if self.board[l][c - 1] == '--' and self.board[l][c - 2] == '--' and self.board[l][c - 3] == '--':
            if not self.CarreAttaquer(l, c - 1) and not self.CarreAttaquer(l, c - 2):
                Deplacements.append(deplacement((l, c), (l, c - 2), self.board, estRock=True))


class RockValide():
    def __init__(self, wrc, brc, wqc, bqc):
        self.wrc = wrc
        self.brc = brc
        self.wqc = wqc
        self.bqc = bqc



class deplacement():
    # Ceci nous sert a imiter un reel plato d'echec. De base notre premier case est(0.0) alors qu'aux echec elle vaut (a.8)
    rangaLigne = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    ligneaRang = {v: k for k, v in rangaLigne.items()}    #On inverse 1er chiffre avec le 2ème chiffre
    fichieraColonne = {"a": 0, "b": 1, "c": 2, "d": 3,
                       "e": 4, "f": 5, "g": 6, "h": 7}
    colonneaFichier = {v: k for k, v in fichieraColonne.items()} #On inverse la lettre avec le numéro

    def __init__(self, carreDepart, carreFin, plato, estEnpassantPossible = False, estRock =False):
        self.ligneDepart = carreDepart[0]      # La 1ère case de depart en ligne
        self.colonneDepart = carreDepart[1]    # La 1ère case de depart en colonne
        self.ligneFin = carreFin[0]            # La dernière case en ligne
        self.colonneFin = carreFin[1]          # La dernière case en colonne
        self.pieceDeplacer = plato[self.ligneDepart][self.colonneDepart] # La pièce qui bouge est la pièce de départ
        self.pieceManger = plato[self.ligneFin][self.colonneFin] # La pièce manger est celle ou arrive la pièce de départ
        #Promotion du Pion
        self.PromotionPion = (self.pieceDeplacer == "wPion" and self.ligneFin == 0) or (self.pieceDeplacer == "bPion" and self.ligneFin == 7)
        #Prise en passant
        self.estEnpassantDeplacement = estEnpassantPossible
        if self.estEnpassantDeplacement:
            self.pieceManger = "wPion" if self.pieceDeplacer == "bPion" else "bPion"
        self.estRock = estRock

        self.IDdeDeplacement = self.ligneDepart * 1000 + self.colonneDepart * 100 + self.ligneFin *10 + self.colonneFin * 1

    #La methode equal va nous etre utile pour verifier si notre deplacement est possible
    def __eq__(self, other):
        if isinstance(other,deplacement):
            return self.IDdeDeplacement == other.IDdeDeplacement
        return False


    def recuperLesNotationsOfficielles(self):
        #Permettre d'afficher dans le shell la notation officiel
        return self.recupererInformationRang(self.ligneDepart, self.colonneDepart) + self.recupererInformationRang(self.ligneFin, self.colonneFin)


    def recupererInformationRang(self, l, c):
        #Permet de recuperer les informations sur la line et la colone
        return self.colonneaFichier[c] + self.ligneaRang[l]

