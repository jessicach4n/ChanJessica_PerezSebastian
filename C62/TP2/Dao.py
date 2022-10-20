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

    def select_from(self, ligne, table) : 
        self.curseur.execute(con.SELECT_FROM%(ligne,table))
        reponse = self.curseur.fetchall()
        return reponse

    def inserer_mot_dictionnaire(self, texte:list):
        for mot in texte:
            self.curseur.execute(con.AJOUTER_MOT_DICTIONNAIRE%(mot))
        self.connexion.commit()

    def update_synonyme(self, requete):
        self.curseur.execute(requete)
        self.connexion.commit()

    def inserer_synonyme(self,idx_mot1:int, idx_mot2:int, fenetre:int, occ:int):
        self.curseur.execute(con.AJOUTER_SYNONYME%(idx_mot1,idx_mot2,fenetre,occ))
        self.connexion.commit()