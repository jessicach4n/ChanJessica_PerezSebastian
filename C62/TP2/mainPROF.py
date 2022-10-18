from sys import argv
from traceback import print_exc
from numpy import array
from entrainement import Entrainement
from prediction import Prediction
from options import options
from dao import Dao
from time import time

QUITTER = 'q'

MESS = f'''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez "{QUITTER}" pour quitter.

'''

def imprimer(scores: list) -> None:
    print()
    for mot, score in scores:
        print(f'{mot} --> {score}')

def demander(d: dict, m: array, verbose: bool) -> None:
    reponse = input(MESS)
    while reponse != QUITTER:
        mot, n, fonc = reponse.split()
        t = time()
        scores = Prediction.predire(d, m, mot, int(n), int(fonc))
        if verbose:
            print(f"Prédiction en {time() - t} secondes.")
        imprimer(scores)
        reponse = input(MESS)

def main() -> int:
    try:
        opts = options()
        with Dao() as dao:
            if opts.b:
                dao.creer_bd()
            else:
                e = Entrainement(opts.t, dao)
                if opts.e:
                    t = time()
                    e.entrainer(opts.enc, opts.chemin)
                    if opts.v:
                        print(f"Entraînement en {time() - t} secondes.")
                else:
                    e.construire_matrice()
                    #print(e.matrice)
                    demander(e.vocabulaire, e.matrice, opts.v)
    except:
        print_exc()
        return 1
    return 0

if __name__ == '__main__':
    quit(main())
