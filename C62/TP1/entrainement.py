import re
import numpy as np
import math

class Entrainement:
    def __init__(self):
        self.texte = []
        self.liste_mots = []
    
    def lire_fichier(self, fichier, encodage):
        f = open(fichier, 'r', encoding=encodage)
        for rangee in f:
            for mot in rangee.split():
                self.texte.append(mot)
                if mot not in self.liste_mots:
                    self.liste_mots.append(mot)
        f.close()
        return len(self.liste_mots)
        
    def creation_matrice(self, fenetre, fichier, encodage):
        taille_m = self.lire_fichier(fichier, encodage)
        m = np.zeros((taille_m, taille_m))
        nb_voisin = math.floor(int(fenetre)/2)
        
        for idx, mot in enumerate(self.texte):
            for i in range(nb_voisin):
                index_mot = idx + 1 + i
                if index_mot < len(self.texte):
                    recherche_a = self.texte[index_mot]
                if recherche_a is not None:
                    index_mot_central = self.liste_mots.index(mot)
                    index_mot = self.liste_mots.index(recherche_a)
                    m[index_mot_central][index_mot] += 1
                    
            for i in range(nb_voisin):
                index_mot_inv = idx - 1 - i
                recherche_b = None
                if index_mot_inv >= 0:
                    recherche_b = self.texte[index_mot_inv]
                if recherche_b is not None:
                    index_mot_central = self.liste_mots.index(mot)
                    index_mot = self.liste_mots.index(recherche_b)
                    m[index_mot_central][index_mot] += 1
                    
        return m
    
        
if __name__ == '__main__':
    e = Entrainement()