import re
import numpy as np

from Utils import Utils

class Entrainement:
    def __init__(self):
        self.__texte = []
        self.__dict_mots = {}
        self.__m = None
    
    @property
    def m(self):
        return self.__m
    
    @property
    def dict_mots(self):
        return self.__dict_mots
    
    def __creer_liste_mots(self, fichier, encodage='utf-8'):
        f = Utils.lire_fichier(fichier, encodage)
        self.__texte = re.findall('\w+', f)
        
        self.__dict_mots = Utils.creer_dict_mots(self.__texte)
        # self.__creer_dict_mots()

    def __creer_dict_mots(self):
        for mot in self.__texte:
            if mot not in self.__dict_mots:
                self.__dict_mots[mot] = len(self.__dict_mots)
        
    def creation_matrice(self, fenetre, fichier, encodage):
        self.__creer_liste_mots(fichier, encodage)
        taille_m = len(self.__dict_mots)
        self.__m = np.zeros((taille_m, taille_m))
        nb_voisin = fenetre//2
        
        for idx, mot in enumerate(self.__texte):
            for i in range(nb_voisin):
                index_mot = idx + 1 + i
                if index_mot < len(self.__texte):
                    recherche = self.__texte[index_mot]

                    index_mot_central = self.__dict_mots[mot]
                    index_mot = self.__dict_mots[recherche]
                    self.__m[index_mot_central][index_mot] += 1
                    
            for i in range(nb_voisin):
                index_mot_inv = idx - 1 - i
                if index_mot_inv >= 0:
                    recherche = self.__texte[index_mot_inv]
                    
                    index_mot_central = self.__dict_mots[mot]
                    index_mot = self.__dict_mots[recherche]
                    self.__m[index_mot_central][index_mot] += 1
                    
    
    
        
if __name__ == '__main__':
    e = Entrainement()
