import re
import numpy as np

from Utils import Utils
from Dao import Dao

'''
PROBLEMS :
1 - CAN'T ACCESS DATABASE TABLE INFORMATION FROM ANOTHER CONTEXT MANAGER
    - In traiter arguments reinitialiser bd
2 - update_synonymeBD for select and update occurences

'''

class Entrainement:
    def __init__(self):
        self.__texte = []
        self.__dict_mots = {}
        self.__m = {}
    
    def update_dictionnaireBD(self, fichier:str, encodage:str='utf-8'):
        f = Utils.lire_fichier(fichier, encodage)
        liste_mots = []
        with Dao() as dao :
            self.__texte = re.findall('\w+', f)
            mots = dao.select_from("mot", "dictionnaire")
            for mot in self.__texte:
                if mot not in mots and mot not in liste_mots:
                    liste_mots.append(mot)
            dao.inserer_mot_dictionnaire(liste_mots)

            self.__liste_mots = dao.select_from('*', 'dictionnaire') 
            for item in self.__liste_mots:
                idx_mot, mot = item
                self.__dict_mots[mot] = idx_mot
                
    def update_synonymeBD(self, fenetre:str):
        with Dao() as dao:

            nb_voisin = fenetre//2
        
            for idx, mot in enumerate(self.__texte):
                for i in range(nb_voisin):
                    index_mot = idx + 1 + i
                    if index_mot < len(self.__texte):
                        recherche = self.__texte[index_mot]

                        index_mot_central = self.__dict_mots[mot]   #
                        index_mot = self.__dict_mots[recherche]     #
                        
                        if (index_mot_central, index_mot, fenetre) not in self.__m.keys():
                            self.__m[(index_mot_central, index_mot, fenetre)] = 0
                        
                        self.__m[(index_mot_central, index_mot, fenetre)] += 1

                       
                for i in range(nb_voisin):
                    index_mot_inv = idx - 1 - i
                    if index_mot_inv >= 0:
                        recherche = self.__texte[index_mot_inv]
                        
                        index_mot_central = self.__dict_mots[mot]   #
                        index_mot = self.__dict_mots[recherche]     #
                        
                        if (index_mot_central, index_mot, fenetre) not in self.__m.keys():
                            self.__m[(index_mot_central, index_mot, fenetre)] = 0
                        
                        self.__m[(index_mot_central, index_mot, fenetre)] += 1
            
            # SELECT CURRENT NUMBER OF OCCURENCE IN THE DATABASE WITH THE KEY
            # ADD THIS OCCURENCE TO DATABASE OCCURENCE
            # UPDATE SYNONYME TABLE
            liste_synonymes = dao.select_from('*', 'synonyme')
            idx_mot1, idx_mot2, f, occurence = liste_synonymes

            if (idx_mot1, idx_mot2, f) in self.__m.keys():
                self.__m[idx_mot1, idx_mot2, f] += occurence
            
            #for syn in self.__m:
                #dao.inserer_synonyme()
            

if __name__ == '__main__':
    e = Entrainement()
