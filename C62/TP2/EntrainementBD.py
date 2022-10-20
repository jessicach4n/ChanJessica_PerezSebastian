from filecmp import clear_cache
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
        mots_bd = []
        with Dao() as dao :
            self.__texte = re.findall('\w+', f)
            
            for tuple_mot in dao.select_from("mot", "dictionnaire"):
                mot = tuple_mot[0]
                mots_bd.append(mot)

            for mot in self.__texte:
                if mot not in mots_bd and mot not in liste_mots:
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

                        index_mot_central = self.__dict_mots[mot]   
                        index_mot = self.__dict_mots[recherche]     
                        
                        if (index_mot_central, index_mot, fenetre) not in self.__m.keys():
                            self.__m[(index_mot_central, index_mot, fenetre)] = 0
                        
                        self.__m[(index_mot_central, index_mot, fenetre)] += 1

                       
                for i in range(nb_voisin):
                    index_mot_inv = idx - 1 - i
                    if index_mot_inv >= 0:
                        recherche = self.__texte[index_mot_inv]
                        
                        index_mot_central = self.__dict_mots[mot]   
                        index_mot = self.__dict_mots[recherche]     
                        
                        if (index_mot_central, index_mot, fenetre) not in self.__m.keys():
                            self.__m[(index_mot_central, index_mot, fenetre)] = 0
                        
                        self.__m[(index_mot_central, index_mot, fenetre)] += 1
            
            liste_synonymes = dao.select_from('*', 'synonyme')
            if len(liste_synonymes) != 0:
                for tuple_synonyme in liste_synonymes:
                    idx_mot1, idx_mot2, f, occurence = tuple_synonyme
                    cle_compose = (idx_mot1, idx_mot2, f)
                    if (cle_compose) in self.__m.keys():
                        self.__m[idx_mot1, idx_mot2, f] += occurence

                        # Do update because it exists in table
                        # Make update constant
                        dao.update_synonyme(f'''
                        UPDATE synonyme
                        SET nb_occurence = {self.__m[idx_mot1, idx_mot2, f]}
                        WHERE
                            idx_mot1 = {idx_mot1} AND
                            idx_mot2 = {idx_mot2} AND
                            taille_fenetre = {f}
                        ''')
                        self.__m.pop((cle_compose))
                        
            for syn in self.__m:
                idx_mot1, idx_mot2, fenetre = syn
                occurence = self.__m[syn]
                dao.inserer_synonyme(idx_mot1, idx_mot2, fenetre, occurence)
