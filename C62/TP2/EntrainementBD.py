import re

from Utils import Utils
from Dao import Dao

class Entrainement:
    def __init__(self):
        self.__texte = []
        self.__dict_mots = {}
        self.__dict_synonymes = {}
    
    def update_dictionnaireBD(self, fichier:str, encodage:str='utf-8'):
        f = Utils.lire_fichier(fichier, encodage)
        liste_mots = []
        mots_bd = {}
        with Dao() as dao :
            self.__texte = re.findall('\w+', f)
            liste_dictionnaire = dao.select_from_dictionnaire()
            
            for idx, mot in liste_dictionnaire:
                mots_bd[mot] = idx

            for mot in self.__texte:
                if mot not in mots_bd:
                    liste_mots.append((len(mots_bd), mot))
                    mots_bd[mot] = len(mots_bd)

            dao.inserer_mot_dictionnaire(liste_mots)
            liste_dictionnaire = dao.select_from_dictionnaire() 

            for tuple_mot in liste_dictionnaire:
                idx_mot, mot = tuple_mot
                self.__dict_mots[mot] = idx_mot
                
    def update_synonymeBD(self, fenetre:str):
        nb_voisin = fenetre//2
    
        for idx, mot in enumerate(self.__texte):
            for i in range(nb_voisin):
                index_mot = idx + 1 + i
                if index_mot < len(self.__texte):
                    recherche = self.__texte[index_mot]

                    index_mot_central = self.__dict_mots[mot]   
                    index_mot = self.__dict_mots[recherche]     
                    
                    if (index_mot_central, index_mot, fenetre) not in self.__dict_synonymes:
                        self.__dict_synonymes[(index_mot_central, index_mot, fenetre)] = 0
                    
                    self.__dict_synonymes[(index_mot_central, index_mot, fenetre)] += 1
                
                index_mot_inv = idx - 1 - i
                if index_mot_inv >= 0:
                    recherche = self.__texte[index_mot_inv]
                    
                    index_mot_central = self.__dict_mots[mot]   
                    index_mot = self.__dict_mots[recherche]     
                    
                    if (index_mot_central, index_mot, fenetre) not in self.__dict_synonymes:
                        self.__dict_synonymes[(index_mot_central, index_mot, fenetre)] = 0
                    
                    self.__dict_synonymes[(index_mot_central, index_mot, fenetre)] += 1
        
        with Dao() as dao:
            liste_synonymes = dao.select_from_synonyme()
            liste_nouveau_synonymes = []
            liste_update_synonymes = []
            
            if len(liste_synonymes) > 0:
                # print(self.__dict_synonymes)
                for tuple_synonyme in liste_synonymes:
                    idx_mot1, idx_mot2, f, occurence = tuple_synonyme
                    cle_compose = (idx_mot1, idx_mot2, f)
                    if (cle_compose) in self.__dict_synonymes:
                        self.__dict_synonymes[idx_mot1, idx_mot2, f] += occurence
                        # print ("going into update")
                        liste_update_synonymes.append((idx_mot1, idx_mot2, f, self.__dict_synonymes[idx_mot1, idx_mot2, f]))
                    else :
                        # print ("going into new")
                        liste_nouveau_synonymes.append((idx_mot1, idx_mot2, f, occurence))
            else:
                for syn in self.__dict_synonymes:
                    idx_mot1, idx_mot2, f = syn
                    occurence = self.__dict_synonymes[syn]
                    liste_nouveau_synonymes.append((idx_mot1, idx_mot2, f, occurence))

            dao.update_synonyme(liste_update_synonymes)
            dao.inserer_synonyme(liste_nouveau_synonymes)
                        

