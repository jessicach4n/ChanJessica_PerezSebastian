import argparse
from sys import argv
from email.policy import default
from tabnanny import verbose
from time import perf_counter
import re

from RechercheBD import Recherche
from EntrainementBD import Entrainement
from Dao import Dao

QUITTER = 'q'

MESS = f'''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez "{QUITTER}" pour quitter.

'''

class LecteurArgs:
    def __init__(self) -> None:
        self.__entrainement = Entrainement()

        parser = argparse.ArgumentParser(description='User input')
        parser.add_argument('-e', action='store_true', help='Executer un entrainement')
        parser.add_argument('-r', action='store_true', help='Executer une recherche')
        parser.add_argument('-b', action='store_true', help='Recreer la base de donnees')
        parser.add_argument('-v', action='store_true', help='Verbose')
        parser.add_argument('-t', nargs='?', type=int, help='Specifier la taille de fenetre')
        parser.add_argument('--enc', nargs='?', help="Specifier l'encodage")
        parser.add_argument('--chemin', nargs='?', help='Specifier le chemin du fichier texte')
        
        self.args = parser.parse_args()

    def __traiter_arguments(self) -> dict:
        with Dao() as dao :
            if self.args.e:
                if self.args.t is None or self.args.enc is None or self.args.chemin is None:
                    return 'Erreur : Entrainement besoin de trois arguments'
                elif self.args.t <= 0 or self.args.enc.lower() not in ['utf-8']:
                    return 'Erreur : Mauvais arguments'
                self.__entrainement.update_dictionnaireBD(self.args.chemin, self.args.enc)
                self.__entrainement.update_synonymeBD(self.args.t)
            
            elif self.args.r:
                if self.args.t is None:
                    return 'Erreur : Recherche besoin argument taille -t'
                self.__afficher_options_recherche(self.args.v)

            elif self.args.b:
                dao.reinitialiser_bd()

    @property
    def traiter_arguments(self):
        return self.__traiter_arguments   
    
    def __afficher_options_recherche(self, verbose) -> None:
        r = ""
        while r != QUITTER:

            r = input(MESS)

            if r == 'q':
                return
                
            reponse = re.findall('\w+', r)
            recherche = Recherche(reponse, self.args.t)
            
            start_time = perf_counter()
            match reponse[2]:
                case '0':
                    recherche.produit_scalaire()
                    end_time = perf_counter()
                case '1':
                    recherche.least_squares()
                    end_time = perf_counter()
                case '2':
                    recherche.city_block()
                    end_time = perf_counter()
                case default:
                    return             
            
            print("")
            recherche.afficher_resultat()
            
            # POUR IMPRIMER LE TEMPS DE CALCUL DES FONCTIONS :
            if verbose:
                print(f"\nTemps écoulé : {end_time - start_time}")
        

 

