from sys import argv
from Entrainement import Entrainement

def interface_usager(fenetre, encodage, path):
    rep = input('''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, 
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez q pour quitter ''')
    entrainement = Entrainement()
    matrice = entrainement.creation_matrice(fenetre, path, encodage)
    print(matrice)
    
    match rep:
        case '0':
            print('Produit scalaire')
        case '1':
            print('Least-squares')
        case '2':
            print('City-block')
        case 'q':
            return rep
    
    interface_usager(fenetre, encodage, path)

def main():
    # fenetre, encodage, path = argv[1:]
    
    fenetre = 5
    encodage = 'utf-8'
    path = 'C:\\Users\\1830222\\Documents\\ChanJessica_PerezSebastian\\C62\\TP1\\textes\\test.txt'
    
    rep = interface_usager(fenetre, encodage, path)
    if rep == 'q':
        quit()
    
        
if __name__ == '__main__':
    main()
    
    
