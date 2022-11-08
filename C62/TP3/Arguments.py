import argparse
import imp
from shutil import ExecError
from time import perf_counter
import re

from RechercheCluster import Recherche
from EntrainementCluster import Entrainement
from Dao import Dao
from Clustering import Clustering
import Constants as con

class Arguments:
    def __init__(self) -> None:
        self.__entrainement = Entrainement()

        parser = argparse.ArgumentParser(description='User input')
        parser.add_argument('-e', action='store_true', help='Executer un entrainement')
        parser.add_argument('-r', action='store_true', help='Executer une recherche')
        parser.add_argument('-b', action='store_true', help='Recreer la base de donnees')
        parser.add_argument('-v', action='store_true', help='Verbose')
        parser.add_argument('-c', action='store_true', help='Executer le clustering')
        parser.add_argument('-n', nargs='?', type=int, help='Nombre maximal de mots à afficher par cluster')
        parser.add_argument('-k', nargs='?', type=int, help='Nombre de centroïdes')
        parser.add_argument('-t', nargs='?', type=int, help='Specifier la taille de fenetre')
        parser.add_argument('--enc', nargs='?', type=str, help="Specifier l'encodage")
        parser.add_argument('--chemin', nargs='?', type=str, help='Specifier le chemin du fichier texte')
        
        self.args = parser.parse_args()

    def traiter_arguments(self) -> None:
        with Dao() as dao :
            if self.args.e:
                if self.args.t is None or self.args.enc is None or self.args.chemin is None:
                    raise Exception('Entrainement besoin de trois arguments')

                elif self.args.t <= 0 or self.args.enc.lower() not in ['utf-8']:
                    raise Exception('Mauvais arguments')
                
                start_time = perf_counter()
                self.__entrainement.update_dictionnaireBD(self.args.chemin, self.args.enc)
                end_time_dictionnaireBD = perf_counter()
                self.__entrainement.update_synonymeBD(self.args.t)
                end_time_synonymeBD = perf_counter()
                
                if self.args.v:
                    print(f"\nTemps écoulé (dictionnaireBD): {end_time_dictionnaireBD - start_time}")
                    print(f"\nTemps écoulé (synonymeBD): {end_time_synonymeBD - start_time}\n")

            elif self.args.r:
                if self.args.t is None:
                    raise Exception('Recherche besoin argument taille -t')
                self.__afficher_options_recherche()
            
            elif self.args.b:
                dao.reinitialiser_bd()

            elif self.args.c:
                if self.args.t is None or self.args.n is None or self.args.k is None:
                    raise Exception('Clustering a besoin de trois arguments')
                c = Clustering(self.args.t, self.args.n, self.args.k)
                
    
    def __afficher_options_recherche(self) -> None:
        r = ""
        while r != con.QUITTER:
            r = input(con.MESS)

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
            
            print("")
            recherche.afficher_resultat()
            
            if self.args.v:
                print(f"\nTemps écoulé (recherche): {end_time - start_time}")
        

 

