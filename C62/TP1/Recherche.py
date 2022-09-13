import numpy as np
import re

from Utils import Utils

class Recherche:
    def __init__(self, entrainement, data):
        self.__matrice = entrainement.m
        self.__dict_mots = entrainement.dict_mots
        self.__dict_stopwords = {}
        self.__scores = []
        self.__mot_recherche = data[0]
        self.__idx_mot_recherche = self.__dict_mots[data[0]]
        self.__limite = int(data[1])
        self.__option = int(data[2])
        self.__decroissant = True
    
    def produit_scalaire(self):
        self.__calcul_score()
    
    def least_squares(self):
        self.__decroissant = False
        self.__calcul_score()
        
    def city_block(self):
        self.__decroissant = False
        self.__calcul_score()
            
    def __calcul_score(self):
        for mot_compare, idx in self.__dict_mots.items():
            match self.__option:
                case 0:
                    score = np.sum(self.__matrice[self.__idx_mot_recherche] * self.__matrice[idx])
                case 1:
                    score = np.sum((self.__matrice[self.__idx_mot_recherche] - self.__matrice[idx])**2)
                case 2:
                    score = np.sum(np.abs(self.__matrice[self.__idx_mot_recherche] - self.__matrice[idx]))
        
            self.__scores.append((score, mot_compare))

    def __creer_dictionnaire_stopwords(self):
        path = ".\\_stopwords\\stopwords_francais.txt"
        f = Utils.lire_fichier(path)      
        texte = re.findall('\w+', f)
        self.__dict_stopwords = Utils.creer_dict_mots(texte)
        
    def afficher_resultat(self):
        self.__creer_dictionnaire_stopwords()
        scores_croissant = sorted(self.__scores, reverse=self.__decroissant)
        resultats = []
        counter = 0
        for score, mot in scores_croissant:
            mot = str(mot)
            score = str(score)
            if counter < self.__limite and self.__mot_recherche != mot and mot not in self.__dict_stopwords:
                resultats.append(mot + " --> " + score)
                counter += 1
            else:
                continue
           
        for resultat in resultats:
            print(resultat)
                
            
            
            
            
            
        
        
