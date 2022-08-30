import sys

def interface_usager(window, encoding, path):
    answer = input('''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, 
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez q pour quitter ''')
    
    match answer:
        case '0':
            print('Produit scalaire')
        case '1':
            print('Least-squares')
        case '2':
            print('City-block')
        case 'q':
            return answer
    
    interface_usager(window, encoding, path)

def main():
    window = str(sys.argv[1])
    encoding = str(sys.argv[2])
    path = str(sys.argv[3])
    
    answer = interface_usager(window, encoding, path)
    if answer == 'q':
        quit()
    
        
if __name__ == '__main__':
    main()
    
    
