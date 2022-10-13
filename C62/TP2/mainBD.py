from ast import arg, arguments
from sys import argv
from time import perf_counter

import argparse
import os

from Entrainement import Entrainement
from Recherche import Recherche
import re

def interface_usager(entrainement, verbose):
    r = ""
    
    while r != 'q':
        
        r = input('''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, 
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez q pour quitter 

''')
        if r == 'q':
            return
        
        reponse = re.findall('\w+', r)
        recherche = Recherche(entrainement, reponse)
        
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

def main():

    # try:
        parser = argparse.ArgumentParser(description='User input')
        parser.add_argument('-e', action='store_true', help='Executer un entrainement')
        parser.add_argument('-r', action='store_true', help='Executer une recherche')
        parser.add_argument('-b', action='store_true', help='Recreer la base de donnees')

        parser.add_argument('-t', nargs='?', type=int, help='Specifier la taille de fenetre')
        parser.add_argument('--enc', nargs='?', help="Specifier l'encodage")
        parser.add_argument('--chemin', nargs='?', help='Specifier le chemin du fichier texte')
        
        args = parser.parse_args()


        
        if args.e:
            if args.t is None or args.enc is None or args.chemin is None:
                print('Error : Needs more arguments')
                return 1
            elif args.t <= 0 or args.enc not in ['utf-8']:
                print('Error : Wrong arguments')
                return 1
            print('works') 

            


    # except:
    #     return 1    
    # return 0
    
        
if __name__ == '__main__':
    quit(main())
    
    
