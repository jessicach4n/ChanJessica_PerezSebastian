from unittest import result
import numpy as np
from sys import argv
from Dao import Dao
class KNN():
    def __init__(self, ch_etiq, enc, nb_voisins, taille_fenetre) -> None:
        self.__dict_mots = {}
        self.__dict_synonymes = {}

        with Dao() as dao:
            self.__creer_dictionnaire_mots(dao)
            self.__creer_dictionnaire_synonyme(dao, taille_fenetre)

        self.__matrice = np.zeros((len(self.__dict_mots), len(self.__dict_mots)))

        self.__creer_matrice()

        
        self.SEP = '\t'
        self.VOTE_SIMPLE = 0
        self.VOTE_DISTANCE = 1

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

    def creation_listes(self, ch, enc):
        with open(ch, encoding = enc) as f:
            lignes = f.read().splitlines()
        # print(lignes)
        noms = lignes[0].split(self.SEP)
        # print(noms)   
        ortho_cgram_liste = {}
        cgram_liste = []
        #on cree ici la liste de association entre ortho et cgram
        for valeur in lignes[1:]:
            ortho = valeur.split(self.SEP)[0]
            cgram = valeur.split(self.SEP)[3]
            if cgram not in cgram_liste:
                cgram_liste.append(cgram)
            
            if ortho not in ortho_cgram_liste.keys():
                ortho_cgram_liste[ortho] = [cgram]
            else :
                # print(type(ortho_cgram_liste))
                ortho_cgram_liste[ortho].append(cgram) 
        # ortho_cgram_liste = np.array(ortho_cgram_liste)
        # cgram_liste = np.array(cgram_liste)
        # print(ortho_cgram_liste)
        # print(cgram_liste)
        return (cgram_liste, ortho_cgram_liste)

    def extraire_caracteristiques(self, ch, enc):
        with open(ch, encoding=enc) as f:
            lignes = f.read().splitlines()
        noms = lignes[0].split(self.SEP)

        caracs = []
        for ligne in lignes[1:]:
            valeurs = []
            for valeur in ligne.split(self.SEP):
                valeurs.append(float(valeur))
            caracs.append(valeurs)
        caracs = np.array(caracs)
        return (noms, caracs)


    def ls(self, p1, p2):
        try :
            idx_p1 = self.__dict_mots[p1]
        except : raise Exception("Le mot desiré n'est pas dans la BD")
        try :
            idx_p2 = self.__dict_mots[p2]
            pos_p2 = self.__matrice[idx_p2]
        except : 
            pos_p2 = np.zeros(self.__matrice.shape)

        pos_p1 = self.__matrice[idx_p1]
        
        return np.sum((pos_p1-pos_p2)**2)

        

    def voter(self, cgram, ortho_cgram, inconnu, k, pond):
        distances = []
        print('distances')
        try:
            vec_inconnu = self.__matrice[self.__dict_mots[inconnu]]
        except: raise Exception("Ce mot n'est pas dans notre base de données")

        for mot, index in self.__dict_mots.items():
            if mot in ortho_cgram and mot != inconnu:
                distances.append((np.sum((self.__matrice[index] - vec_inconnu)**2),mot,ortho_cgram[mot][0]))
        print(type(ortho_cgram))
        # for i in ortho_cgram.keys():
        #     dist = self.ls(inconnu, ortho_cgram[i][0])
        #     distances.append((dist, ortho_cgram[i][0]))
        distances = sorted(distances)[:k]

        print(distances)
        
        print('votes')
        votes = np.zeros(len(cgram))
        for i in range(len(distances)):
            distance,mot,etiq = distances[i]
            etiq = cgram.index(etiq)
            if pond == self.VOTE_SIMPLE:
                votes[etiq] += 1
            elif pond == self.VOTE_DISTANCE:
                votes[etiq] += 1/(distance+1)**2

        resultats = []  
        for i in range(len(votes)):
            resultats.append((cgram[i], votes[i]))

        return resultats

    def norm_somme(self,caracs):
        return caracs/np.sum(caracs, axis=1)[:, None]

def main():
    #* ch_etiq, ch_carac, enc, poids, long, larg, haut, k, pond = argv[1:]
    ch_etiq, enc = argv[1:]
    knn = KNN(ch_etiq,enc, 3, 5)
    cgram, ortho_cgram = knn.creation_listes(ch_etiq, enc)
    print(ortho_cgram)
    print(cgram)
    #*noms_caracs, caracs = extraire_caracteristiques(ch_carac, enc)
    #print(noms_caracs)
    #print(caracs)
    #*caracs = norm_somme(caracs)
    #print(caracs)
    
    #* inconnu = np.array((poids, long, larg, haut), dtype=float)
    inconnu = 'fleur'
    #print(inconnu)

    k = int(6)
    pond = int(0)

    votes = knn.voter(cgram, ortho_cgram, inconnu, k, pond)

    print(f'this is votes {votes}')

    return 0

if __name__ == '__main__':
        quit(main())