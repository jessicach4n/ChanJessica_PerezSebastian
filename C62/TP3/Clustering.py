import random
import numpy as np
from time import perf_counter
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
        self.__centroides = np.zeros((nbre_centroides,len(self.__dict_mots) ), dtype=float)
        # self.__nouveux_centroides = np.zeros((len(self.__dict_mots), nbre_centroides), dtype=float)
        # self.__matrice_asso_mot_cluster = np.zeros((len(self.__dict_mots),2))

        self.__creer_matrice()
        self.__creer_centroides_depart()
        self.__calculer_cluster()
        self.__traitement_clustering()

    def __traitement_clustering(self) -> None:
        counter = 0
        nb_iteration = 0
        max_iter = 3 # Après aucun changement
        nb_changement = len(self.__matrice)
        # aucun_changement = np.array_equal(self.__ancien_cluster, self.__cluster)
        # while aucun_changement and counter < max_iter: 
        while nb_changement > 0:
            temps_depart = perf_counter()
            population_cluster = self.__recalculer_centroide()
            nb_changement = self.__calculer_cluster()
            # if aucun_changement: 
                # counter += 1 
            
            nb_iteration += 1
            temps_fin = perf_counter()
            
            # population_cluster = []
            # for centroide in range(self.__nbre_centroides):
            #     population_cluster.append(np.count_nonzero(self.__cluster == centroide))
            #     # print(f'self centroides {self.__centroides}')
                # print( f'popuplation cluster :  {population_cluster}')
                # print( f'centroide  :  {centroide}')
            # nb_changement = '#'
            self.__print_message(nb_iteration, temps_fin - temps_depart, nb_changement, population_cluster)


    def __print_message(self, nb_iteration, temps, nb_changement, population_cluster) -> None:
        separateur = "\n***********************************************************************\n"
        message = f"Iteration {nb_iteration} effectuée en {temps} secondes ({nb_changement} changements)\n"
        for idx, cluster in enumerate(population_cluster):
            message += f"\nIl y a {cluster} mots appartenant au centroide {idx}"
            
        print(separateur)
        print(message)
        print(separateur)

    def __creer_centroides_depart(self) -> None:
        random_values = []
        i = 0
        while i < self.__nbre_centroides:
            idx_mot = random.randrange(len(self.__dict_mots))
            if idx_mot not in random_values:
                random_values.append(idx_mot)
                i += 1
        for idx in range(self.__nbre_centroides) :
            self.__centroides[idx] = self.__matrice[random_values[idx]]

        # print('position centroides depart \n')
        # print(self.__centroides)

    def __calculer_cluster(self) -> None:
        self.__cluster  = np.arange(len(self.__matrice))
        # print(f'self.__cluster : {self.__cluster}')
        for i in range(len(self.__dict_mots)):
            d = [] 
            for c in self.__centroides:
                d.append(np.sum((self.__matrice - c)**2))

            centroide = d.index(min(d))
            self.__cluster[i] = centroide

        # print(f'self.__cluster 2 : {self.__cluster}')
        nb_changement = np.sum(np.not_equal(self.__ancien_cluster, self.__cluster))
        self.__ancien_cluster = self.__cluster
        # print(" chaque mots appartient à quel cluster \n")
        # print(self.__centroides)
        return nb_changement

    def __recalculer_centroide(self):
        self.__centroides = np.zeros((self.__nbre_centroides,len(self.__dict_mots) ), dtype=float)
        decompte = np.zeros(self.__nbre_centroides)

        for i in range(len(self.__matrice)):
            centroide = self.__cluster[i]
            self.__centroides[centroide] += self.__matrice[i]
            decompte[centroide] += 1 
        for i in range(self.__nbre_centroides):
            if decompte[i] > 0 :
                self.__centroides[i] /= decompte[i]

        return decompte

        # print('position de nouveaux centroide \n')
        # print(self.__centroides)

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

