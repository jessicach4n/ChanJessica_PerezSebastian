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
        self.__centroides = np.zeros((nbre_centroides,len(self.__dict_mots) ), dtype=float)
        self.__nouveux_centroides = np.zeros((len(self.__dict_mots), nbre_centroides), dtype=float)
        self.__matrice_asso_mot_cluster = np.zeros((len(self.__dict_mots),2))


        for id_mot, id_occurence, nb_occurence in self.__liste_synonymes:
            self.__matrice[id_mot,id_occurence] = nb_occurence

        self.__creer_matrice()
        self.__creer_centroides_depart()
        self.calculer_cluster()
        self.__recalculer_centroide()
 


    def __creer_centroides_depart(self) -> None:
        random_values = []
        for _ in range(self.__nbre_centroides):
            idx_mot = random.randrange(len(self.__dict_mots))
            if idx_mot not in random_values:
                random_values.append(idx_mot)
        for idx in range(self.__nbre_centroides) :
            self.__centroides [idx]= self.__matrice[random_values[idx]]
         #print etat initial des centroides. 
        print(self.__centroides)

        # Trouver les premiers centroides avec des valeurs de mot aléatoires
        #self.__centroides contient les coordonnées de n centroides 
        # for colonne in range(self.__centroides.shape[1]):
        #     self.__centroides[:, colonne] = self.__matrice[random_values[colonne]]

     

    def calculer_cluster(self) -> None:

        self.clusters  = np.arange(len(self.__matrice))
        for i in range(len(self.__dict_mots)):
            d = [] 
            for c in self.__centroides:
                d.append(np.sum((self.__matrice - c)**2))

            centroide = d.index(min(d))
            self.clusters[i] = centroide
      

        #distances = np.zeros((self.__centroides.shape))
        # for idx_centroide in range(self.__centroides.shape[1]):
        #     for idx_mot in range(self.__centroides.shape[0]):
        #         distance = np.sum((self.__matrice[idx_centroide] - self.__matrice[idx_mot])**2)
        #         distances[idx_mot][idx_centroide] = distance

        # self.__associer_mot_a_cluster(self.clusters)
        #print l'appartenace donc chaque mot appartient a quel centroide 
        print(self.clusters)
        # print(self.__matrice_asso_mot_cluster)

    # def __associer_mot_a_cluster(self, matrice_distance_mot_centroide:np.array):
    #     for idx_mot_bd in range(matrice_distance_mot_centroide.shape[0]):
    #         #if too slow, make a list at line 51 ti avoid doing argmin
    #         centroide_plus_proche = np.argmin(matrice_distance_mot_centroide[idx_mot_bd])
    #         self.__matrice_asso_mot_cluster[idx_mot_bd][1] = centroide_plus_proche
    #         self.__matrice_asso_mot_cluster[idx_mot_bd][0] = idx_mot_bd    
            
        # print(self.__matrice_asso_mot_cluster)

    def __recalculer_centroide(self):
 
        self.__centroides = np.zeros((self.__nbre_centroides,len(self.__dict_mots) ), dtype=float)
        decompte = np.zeros(self.__nbre_centroides)

        for i in range(len(self.__matrice)):
            centroide = self.clusters[i]
            self.__centroides[centroide] += self.__matrice[i]
            decompte[centroide] += 1 
        for i in range(self.__nbre_centroides):
            if decompte[i] > 0 :
                self.__centroides[i] /= decompte[i]

        # for centroide in range(self.__nbre_centroides):
        #     total_adition_position_mots = np.zeros((1, len(self.__dict_mots)))
        #     nb_elements_dans_cluster = 0


        #     for idx_mot_bd in range(matrice_asso_mot_centroide.shape[0]):
        #         if(matrice_asso_mot_centroide[idx_mot_bd][1] == centroide):
        #             nb_elements_dans_cluster +=1
        #             # total_adition_position_mots += self.__matrice[idx_mot_bd]
        #             total_adition_position_mots = total_adition_position_mots + self.__matrice[idx_mot_bd]
        #     totalavg= total_adition_position_mots /nb_elements_dans_cluster
        #     self.__nouveux_centroides[:, centroide] = totalavg

        # print(self.__nouveux_centroides)

       #print les centroides transformés
        print(self.__centroides)
        # print((matrice_asso_mot_centroide[:,1] == 0).sum())
        
        #eereur. 
        #find size of matrix where centroiide = centroide then append each row to it then mamke an avg on it. 


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

