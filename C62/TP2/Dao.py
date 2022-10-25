import sqlite3
import traceback
import Constants as con

CHEMIN_BD = 'synonymes.db'
FK_ON = 'PRAGMA foreign_keys = 1'

class Dao:
    def __init__(self) -> None:
        self.chemin = CHEMIN_BD

    def __enter__(self): 
        self.connecter()
        return self

    def __exit__ (self,exc_type,exc_value, exc_tb):
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
    
    def creer_bd(self): 
        self.curseur.execute(con.CREATION_TABLE_DICTIONNAIRE)
        self.curseur.execute(con.CREATION_TABLE_SYNONIME)

    def reinitialiser_bd(self):
        self.curseur.execute(con.DROP_TABLE_SYNONYME)
        self.curseur.execute(con.DROP_TABLE_DICTIONNAIRE)
        self.creer_bd()

    def deconnecter(self):
        self.curseur.close()
        self.connexion.close()

    def select_from_dictionnaire(self) : 
        self.curseur.execute(con.SELECT_FROM_DICTIONNAIRE)
        reponse = self.curseur.fetchall()
        return reponse

    def select_from_synonyme(self) : 
        self.curseur.execute(con.SELECT_FROM_SYNONYME)
        reponse = self.curseur.fetchall()
        return reponse

    def select_from_synonyme_where(self, condition):
        self.curseur.execute(con.SELECT_FROM_SYNONYME_WHERE,(condition))
        reponse = self.curseur.fetchall()
        return reponse

    def select_count_synonyme(self, condition):
        self.curseur.execute(con.SELECT_COUNT_SYNONYME,(condition))
        reponse = self.curseur.fetchall()
        return reponse

    def inserer_mot_dictionnaire(self, liste_mots:list):
        self.curseur.executemany(con.AJOUTER_MOT_DICTIONNAIRE,(liste_mots))
        self.connexion.commit()

    def update_synonyme(self, liste_update_synonyme):
        self.curseur.executemany(con.UPDATE_SYNONYME,(liste_update_synonyme))
        self.connexion.commit()

    def inserer_synonyme(self,liste_nouveau_synonyme):
        self.curseur.executemany(con.AJOUTER_SYNONYME,(liste_nouveau_synonyme))
        self.connexion.commit()