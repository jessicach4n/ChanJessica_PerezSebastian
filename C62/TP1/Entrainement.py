import re
import numpy as np

class Entrainement:
    def __init__(self):
        self.texte = []
        self.liste_mots = []
        self.dict_mots = {}
    
    def lire_fichier(self, fichier, encodage):
        f = open(fichier, 'r', encoding=encodage)
        s = f.read()
        f.close()
        return s
    
    def creer_liste_mots(self, fichier, encodage='utf-8'):
        f = self.lire_fichier(fichier, encodage)
        f = f.lower()
        self.texte = re.findall('\w+', f)

        for mot in self.texte:
            if mot not in self.dict_mots:
                self.dict_mots[mot] = len(self.dict_mots)
        
    def creation_matrice(self, fenetre, fichier, encodage):
        self.creer_liste_mots(fichier, encodage)
        taille_m = len(self.dict_mots)
        self.m = np.zeros((taille_m, taille_m))
        nb_voisin = fenetre//2
        
        for idx, mot in enumerate(self.texte):
            for i in range(nb_voisin):
                index_mot = idx + 1 + i
                if index_mot < len(self.texte):
                    recherche = self.texte[index_mot]

                    index_mot_central = self.dict_mots[mot]
                    index_mot = self.dict_mots[recherche]
                    self.m[index_mot_central][index_mot] += 1
                    
            for i in range(nb_voisin):
                index_mot_inv = idx - 1 - i
                if index_mot_inv >= 0:
                    recherche = self.texte[index_mot_inv]
                    
                    index_mot_central = self.dict_mots[mot]
                    index_mot = self.dict_mots[recherche]
                    self.m[index_mot_central][index_mot] += 1
                    
     
    
        
if __name__ == '__main__':
    e = Entrainement()
