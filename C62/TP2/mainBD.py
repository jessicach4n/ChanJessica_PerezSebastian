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
    try:
        arguments = argv[1:]
        opt_entrainement = '-e'
        opt_recherche = '-r'
        param_taille = '-t'
        param_encodage = '--enc'
        param_chemin = '--chemin'
        
        mode_entrainement = False
        mode_recherche = False
        mode_BD = False

        
        if mode_entrainement:
            entrainement = Entrainement()
            # entrainement.creation_matrice(int(fenetre), path, encodage)
            # interface_usager(entrainement, int(verbose))
        elif mode_recherche:
            pass
        elif mode_BD:
            pass
        else:
            pass

        # if len(argv) == 5:
        #     fenetre, encodage, path, verbose = argv[1:]
        # else:
        #     fenetre, encodage, path = argv[1:]
        #     verbose = 0
        

    except:
        return 1    
    return 0
    
        
if __name__ == '__main__':
    quit(main())
    
    