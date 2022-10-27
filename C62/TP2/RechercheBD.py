import numpy as np
import re

from Utils import Utils
from Dao import Dao

class Recherche:
    def __init__(self, data, taille_fenetre):
        self.__dict_stopwords = {}
        self.__dict_synonymes = {}
        self.__dict_mots = {}
        self.__scores = []
        self.__mot_recherche = data[0]
        self.__limite = int(data[1])
        self.__option = int(data[2])
        self.__decroissant = True
        
        with Dao() as dao:
            liste_mots = dao.select_from_dictionnaire()
            for tuple_mot in liste_mots:
                idx, mot = tuple_mot
                self.__dict_mots[mot] = idx

            condition = (taille_fenetre)
            print(f" taille fenetre : {condition}")
            self.__liste_synonymes = dao.select_from_synonyme_where(condition)
            
            # demander a la base de données de faire ça
            for tuple_synonyme in self.__liste_synonymes:
                    idx_mot1, idx_mot2, occurence = tuple_synonyme
                    cle_compose = (idx_mot1, idx_mot2, taille_fenetre)
                    self.__dict_synonymes[cle_compose] = occurence

            d = {}
            for id, mot in dao.select_from_dictionnaire():
                d[mot] = id        

            self.__matrice = np.zeros((len(d), len(d)))
            print (len(self.__matrice))

            for id_mot, id_concurrenre, nb_occurence in self.__liste_synonymes:
                self.__matrice [id_mot,id_concurrenre] = nb_occurence
            

        self.__idx_mot_recherche = self.__dict_mots[self.__mot_recherche]
        self.__creer_matrice()

    def produit_scalaire(self):
        self.__calcul_score()
    
    def least_squares(self):
        self.__decroissant = False
        self.__calcul_score()
        
    def city_block(self):
        self.__decroissant = False
        self.__calcul_score()
    
    def __creer_matrice(self):
        for cle_compose in self.__dict_synonymes:
            idx_mot1, idx_mot2, f = cle_compose
            nb_occurence = self.__dict_synonymes[cle_compose]
            self.__matrice[idx_mot1][idx_mot2] = nb_occurence

    def __calcul_score(self):
        for mot_compare, idx in self.__dict_mots.items():
            score = 0
            match self.__option:
                case 0:
                    score = np.sum(self.__matrice[self.__idx_mot_recherche] * self.__matrice[idx])
                case 1:
                    score = np.sum((self.__matrice[self.__idx_mot_recherche] - self.__matrice[idx])**2)
                case 2:
                    score = np.sum(np.abs(self.__matrice[self.__idx_mot_recherche] - self.__matrice[idx]))
        
            self.__scores.append((score, mot_compare))

    def __creer_dictionnaire_stopwords(self):
        path = "../_stopwords/stopwords_francais.txt"
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
                
            
            
            
            
            
        
        
