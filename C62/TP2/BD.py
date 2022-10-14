from curses.ascii import CR
import sqlite3

CHEMINBD = 'synonymes.db'
# FOREIGN_KEYS = 'PRAGMA foreign_keys = 1'

CREER_SYNONYME = '''
CREATE TABLE IF NOT EXISTS synonyme
(
    id INT PRIMARY KEY NOT NULL,
    mot CHAR(20) UNIQUE  NOT NULL
)
'''

def connecter(chemin_bd):
    connexion = sqlite3.connect(chemin_bd)
    curseur = connexion.cursor()
    # curseur.execute(FOREIGN_KEYS)
    
    return connexion, curseur

def deconnecter(connexion, curseur): # Fermer la ressource
    curseur.close()
    connexion.close()

def main():
    conn, cur = connecter(CHEMINBD)