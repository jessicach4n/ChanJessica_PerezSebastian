from unittest import result
import numpy as np
from sys import argv

SEP = '\t'
VOTE_SIMPLE = 0
VOTE_DISTANCE = 1

def extraire_etiquettes(ch, enc):
    with open(ch, encoding = enc) as f:
        lignes = f.read().splitlines()
    # print(lignes)
    noms = lignes[0].split(SEP)
    # print(noms)   
    ortho_cgram_liste = []
    cgram_liste = []
    #on cree ici la liste de association entre ortho et cgram
    for valeur in lignes[1:]:
        ortho = valeur.split(SEP)[0]
        cgram = valeur.split(SEP)[3]
        if cgram not in cgram_liste:
            cgram_liste.append(cgram)
        ortho_cgram_liste.append([ortho,cgram])
    ortho_cgram_liste = np.array(ortho_cgram_liste)
    # print(ortho_cgram_liste)
    print(cgram_liste)
    return (noms, ortho_cgram_liste)

def extraire_caracteristiques(ch, enc):
    with open(ch, encoding=enc) as f:
        lignes = f.read().splitlines()
    noms = lignes[0].split(SEP)

    caracs = []
    for ligne in lignes[1:]:
        valeurs = []
        for valeur in ligne.split(SEP):
            valeurs.append(float(valeur))
        caracs.append(valeurs)
    caracs = np.array(caracs)
    return (noms, caracs)


def ls(p1, p2):
    return np.sum((p1-p2)**2)

def voter(noms_etiqs, etiqs, caracs, inconnu, k, pond):
    distances = []
    for i in range(len(caracs)):
        dist = ls(inconnu, caracs[i])
        distances.append((dist, etiqs[i]))
    distances = sorted(distances)[:k]
    
    votes = np.zeros(len(noms_etiqs))
    for i in range(len(distances)):
        distance, etiq = distances[i]
        if pond == VOTE_SIMPLE:
            votes[etiq] += 1
        elif pond == VOTE_DISTANCE:
            votes[etiq] += 1/(distance+1)**2

    resultats = []  
    for i in range(len(votes)):
        resultats.append((noms_etiqs[i], votes[i]))

    return resultats

def norm_somme(caracs):
    return caracs/np.sum(caracs, axis=1)[:, None]

def main():
    #! ch_etiq, ch_carac, enc, poids, long, larg, haut, k, pond = argv[1:]
    ch_etiq, enc = argv[1:]
    noms_etiqs, etiqs = extraire_etiquettes(ch_etiq, enc)
    #print(noms_etiqs)
    #print(etiqs)
    
    #!noms_caracs, caracs = extraire_caracteristiques(ch_carac, enc)
    #print(noms_caracs)
    #print(caracs)
    #!caracs = norm_somme(caracs)
    #print(caracs)
    
    #! inconnu = np.array((poids, long, larg, haut), dtype=float)
    #print(inconnu)

    #! k = int(k)
    #! pond = int(pond)

    #! votes = voter(noms_etiqs, etiqs, caracs, inconnu, k, pond)
    #! print(votes)

    return 0

if __name__ == '__main__':
    quit(main())