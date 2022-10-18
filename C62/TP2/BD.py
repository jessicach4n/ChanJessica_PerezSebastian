from curses.ascii import CR
import sqlite3

class BD:
    def __init__(self) -> None:
        __CHEMINBD = 'synonymes.db'
        # FOREIGN_KEYS = 'PRAGMA foreign_keys = 1'

        __CREER_SYNONYME = '''
        CREATE TABLE IF NOT EXISTS synonyme
        (
            id INT PRIMARY KEY NOT NULL,
            mot CHAR(20) UNIQUE  NOT NULL
        )
        '''

    def __connecter(chemin_bd):
        connexion = sqlite3.connect(chemin_bd)
        curseur = connexion.cursor()
        # curseur.execute(FOREIGN_KEYS)
        
        return connexion, curseur

    def __deconnecter(connexion, curseur): # Fermer la ressource
        curseur.close()
        connexion.close()

    # CHANGER POUR ÉCRIRE DANS LA BD POUR TABLE DICTIONNAIRE
    def __inserer_dictionnaireBD(texte:list):
        dictionnaire = {}
        for mot in texte:
            if mot not in dictionnaire:
                dictionnaire[mot] = len(dictionnaire)


    # FONCTION POUR INSÉRER DANS TABLE SYNONYME
    def __inserer_synonymeBD(idx_mot1:int, idx_mot2:int, fenetre:int, occ:int):
        pass
    
def main():
    bd = BD()
    conn, cur = bd.__connecter(bd.__CHEMINBD)