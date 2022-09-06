from sys import argv
from Entrainement import Entrainement
from Recherche import Recherche
from time import perf_counter
import re

def interface_usager(fenetre, entrainement):
    rep = ""
    
    while rep != 'q':
    
        rep = input('''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, 
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez q pour quitter 

''')
        if rep == 'q':
            return
        
        reponse = re.findall('\w+', rep)
        recherche = Recherche(entrainement, reponse)

        start_counter = perf_counter()
        match reponse[2]:
            case '0':
                recherche.produit_scalaire()
                end_counter = perf_counter()
            case '1':
                recherche.least_squares()
                end_counter = perf_counter()
            case '2':
                recherche.city_block()
                end_counter = perf_counter()
            case default:
                return             
    
        start_counter_aff = perf_counter()
        recherche.afficher_resultat()
        end_counter_aff = perf_counter()
        print(f"time fonction : {end_counter-start_counter}")
        print(f"time aff : {end_counter_aff-start_counter_aff}")

def main():
    fenetre, encodage, path = argv[1:]
    # fenetre = 5
    # encodage = 'utf-8'
    # path = 'C:\\Users\\1830222\\Documents\\ChanJessica_PerezSebastian\\C62\\TP1\\textes\\test.txt'
    
    entrainement = Entrainement()
    entrainement.creation_matrice(int(fenetre), path, encodage)

    rep = interface_usager(fenetre, entrainement)
    if rep == 'q':
        quit()
    
        
if __name__ == '__main__':
    main()
    
    
