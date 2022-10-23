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
            liste_mots = dao.select_from('*', 'dictionnaire')
            for tuple_mot in liste_mots:
                idx, mot = tuple_mot
                self.__dict_mots[mot] = idx

            condition = 'taille_fenetre = ' + str(taille_fenetre)
            self.__liste_synonymes = dao.select_from_where('idx_mot1, idx_mot2, nb_occurence', 'synonyme', condition)
            for tuple_synonyme in self.__liste_synonymes:
                    idx_mot1, idx_mot2, occurence = tuple_synonyme
                    cle_compose = (idx_mot1, idx_mot2, taille_fenetre)
                    self.__dict_synonymes[cle_compose] = occurence

        self.__idx_mot_recherche = self.__dict_mots[self.__mot_recherche]
   

    def produit_scalaire(self):
        self.__calcul_score()
    
    def least_squares(self):
        self.__decroissant = False
        self.__calcul_score()
        
    def city_block(self):
        self.__decroissant = False
        self.__calcul_score()
            
    def __calcul_score(self):
        with Dao() as dao:
            for mot_compare, idx in self.__dict_mots.items():
                score = 0
                match self.__option:
                    case 0:
                        condition = f'''
                        idx_mot1 = {idx} 
                        OR idx_mot2 = {idx} 
                        AND idx_mot1 = {self.__idx_mot_recherche} 
                        OR idx_mot2 = {self.__idx_mot_recherche}
                        '''
                        
                        occurences = np.array(dao.select_from_where('nb_occurence', 'synonyme', condition))
                        score = np.sum(occurences)

                        # MULTIPLY WHAT ???
                        #score = np.sum(self.__matrice[self.__idx_mot_recherche] * self.__matrice[idx])
                    case 1:
                        print('least_squares')
                        #score = np.sum((self.__matrice[self.__idx_mot_recherche] - self.__matrice[idx])**2)
                    case 2:
                        print('city_block')
                        #score = np.sum(np.abs(self.__matrice[self.__idx_mot_recherche] - self.__matrice[idx]))
            
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
                
            
            
            
            
            
        
        
