from time import perf_counter
import numpy as np

class Recherche:
    def __init__(self, entrainement, data):
        self.matrice = entrainement.m
        self.dict_mots = entrainement.dict_mots
        self.scores = []
        self.idx_mot_recherche = self.dict_mots[data[0]]
        self.limite = data[1]
        self.option = data[2]
        self.decroissant = True
    
    def produit_scalaire(self):
        for mot_compare, idx in self.dict_mots.items():
            score = np.sum(self.matrice[self.idx_mot_recherche] * self.matrice[idx])
            self.scores.append((score, mot_compare))
        # self.calcul_score()
    
    def least_squares(self):
        self.decroissant = False
        for mot_compare, idx in self.dict_mots.items():
            score = np.sum(np.power(self.matrice[self.idx_mot_recherche] - self.matrice[idx], 2))
            self.scores.append((score, mot_compare))
        # self.calcul_score()
        
    def city_block(self):
        self.decroissant = False
        for mot_compare, idx in self.dict_mots.items():
            score = np.sum(np.abs(self.matrice[self.idx_mot_recherche] - self.matrice[idx]))
            self.scores.append((score, mot_compare))
        # self.calcul_score()
            
    # def calcul_score(self):
        
    #     for mot_compare, idx in self.dict_mots.items():
    #         match self.option:
    #             case 0:
    #                 score = np.sum(self.matrice[self.idx_mot_recherche] * self.matrice[idx])
    #             case 1:
    #                 score = np.sum(np.power(self.matrice[self.idx_mot_recherche] - self.matrice[idx], 2))
    #             case 2:
    #                 score = np.sum(np.abs(self.matrice[self.idx_mot_recherche] - self.matrice[idx]))
        
    #         self.scores.append((score, mot_compare))
        
    def chercher_cle(self, dictionnaire, v):
        for cle, valeur in dictionnaire.items():
            if v == valeur:
                return cle

    def afficher_resultat(self):
        scores_croissant = sorted(self.scores, reverse=self.decroissant)
        resultats = []
        counter = 0
        for score, mot in scores_croissant:
            if counter < int(self.limite):
                resultats.append(str(mot) + " --> " + str(score))
                counter += 1
            else:
                break
           
        for resultat in resultats:
            print(resultat)
                
            
            
            
            
            
        
        
