import sqlite3
import traceback

CHEMIN_BD = 'cooccurrences.db'
FK_ON = 'PRAGMA foreign_keys = 1'

class Dao():
    def __init__(self):
        self.chemin = CHEMIN_BD

    def __enter__(self):
        self.connecter()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.deconnecter()
        if isinstance(exc_value, Exception):
            trace = traceback.format_exception(exc_type, exc_value, exc_tb)
            print(''.join(trace))
            return False
        return True

    def connecter(self):
        self.connexion = sqlite3.connect(self.chemin)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(FK_ON)

    def deconnecter(self):
        self.curseur.close()
        self.connexion.close()