from sys import argv
from time import perf_counter

import argparse

from Entrainement import Entrainement
from Recherche import Recherche
from LecteurArgs import LecteurArgs
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

    options = {
        'Entrainement' : Entrainement,
        'Recherche' : Recherche,
        'BD' : 'BD'
    }
    
    la = LecteurArgs()
    result = la.traiter_arguments()
    
    print(result)

    # except:
    #     return 1    
    # return 0
    
        
if __name__ == '__main__':
    quit(main())
    
    
