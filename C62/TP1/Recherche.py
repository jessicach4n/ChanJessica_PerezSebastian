class Recherche:
    def __init__(self, entrainement, data):
        self.matrice = entrainement.m
        self.dict_mots = entrainement.dict_mots
        self.dict_score = dict()
        self.mot_recherche = data[0]
        self.limite = data[1]
        self.decroissant = True
    
    def produit_scalaire(self):
        idx_mot_recherche = self.dict_mots[self.mot_recherche]
        for idx, rangee in enumerate(self.matrice):
            score = sum(self.matrice[idx_mot_recherche] * self.matrice[idx])
            mot_compare = self.chercher_cle(self.dict_mots, idx)
            self.dict_score[mot_compare] = score
    
    def least_squares(self):
        self.decroissant = False
        print("ls")
    
    def city_block(self):
        self.decroissant = False

        print("cb")
    
    def chercher_cle(self, dictionnaire, v):
        for cle, valeur in dictionnaire.items():
            if v == valeur:
                return cle

    def afficher_resultat(self):
        scores_croissant = sorted(self.dict_score.values(), reverse=self.decroissant)
        resultats = []
        counter = 0
        for score in scores_croissant:
                cle = self.chercher_cle(self.dict_score, score)
                resultats.append(str(cle) + " --> " + str(score))
            
        for resultat in resultats:
            if counter < int(self.limite):
                print(resultat)
            counter += 1
                
            
            
            
            
            
        
        
