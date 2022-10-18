import re
import numpy as np

from Utils import Utils

class Entrainement:
    def __init__(self):
        self.__texte = []
    
    def __creer_structures_mots(self, fichier, encodage='utf-8'):
        f = Utils.lire_fichier(fichier, encodage)
        self.__texte = re.findall('\w+', f)
        Utils.inserer_dictionnaireBD(self.__texte)

    def creation_dictionnaireBD(self, fenetre, fichier, encodage):
        self.__creer_structures_mots(fichier, encodage)
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
    
    def creation_synonymeBD(self):
        pass
        
if __name__ == '__main__':
    e = Entrainement()
