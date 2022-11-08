import random
import numpy as np
from Utils import Utils
from Dao import Dao
from RechercheCluster import Recherche

class Clustering:
    def __init__(self, taille_fenetre:int, nbre_mots:int, nbre_centroides:int) -> None:
        self.__dict_synonymes = {}
        self.__dict_mots = {}
        self.__nbre_mots = nbre_mots
        self.__nbre_centroides = nbre_centroides

        with Dao() as dao:
            self.__creer_dictionnaire_mots(dao)
            self.__creer_dictionnaire_synonyme(dao, taille_fenetre)

        self.__matrice = np.zeros((len(self.__dict_mots), len(self.__dict_mots)))
        self.__centroides = np.zeros((len(self.__dict_mots), nbre_centroides), dtype=float)

        for id_mot, id_occurence, nb_occurence in self.__liste_synonymes:
            self.__matrice[id_mot,id_occurence] = nb_occurence

        self.__creer_matrice()
        self.__creer_centroides_depart()

    def __creer_centroides_depart(self) -> None:
        random_values = []
        for _ in range(self.__nbre_centroides):
            idx_mot = random.randrange(len(self.__dict_mots))
            if idx_mot not in random_values:
                random_values.append(idx_mot)

        for colonne in range(self.__centroides.shape[1]):
            self.__centroides[:, colonne] = self.__matrice[random_values[colonne]]

        self.__least_square()

    def __least_square(self) -> None:
        counterdistance = 0
        # clusters = {
        #     'cluster1' : [],
        #     'cluster2' : [],
        #     'cluster3' : [],
        #     'cluster4' : []
        # }

        distances = np.zeros((self.__centroides.shape))
        for idx_centroide in range(self.__centroides.shape[1]):
            for idx_mot in range(self.__centroides.shape[0]):
                distance = np.sum((self.__matrice[idx_centroide] - self.__matrice[idx_mot])**2)
                distances[idx_mot,idx_centroide] = distance
        
       
                # if distance is not None or distance < best_distance:
                #     best_distance = distance
                # elif distance is None:
                #     best_distance = distance
        print(distances)
            

        #         counterdistance+=1
        # print(f'counter distance : {counterdistance}')
        # print(f'centroide size : {self.__centroides.size}')


    def __creer_dictionnaire_mots(self, dao:Dao) -> None:
        for id, mot in dao.select_from_dictionnaire():
            self.__dict_mots[mot] = id

    def __creer_dictionnaire_synonyme(self, dao:Dao, taille_fenetre:int) -> None:
        self.__liste_synonymes = dao.select_from_synonyme_where(taille_fenetre)
        for tuple_synonyme in self.__liste_synonymes:
            idx_mot1, idx_mot2, occurence = tuple_synonyme
            cle_compose = (idx_mot1, idx_mot2, taille_fenetre)
            self.__dict_synonymes[cle_compose] = occurence

    def __creer_matrice(self) -> None:
        for cle_compose in self.__dict_synonymes:
            idx_mot1, idx_mot2, f = cle_compose
            nb_occurence = self.__dict_synonymes[cle_compose]
            self.__matrice[idx_mot1][idx_mot2] = nb_occurence

