import sqlite3
import traceback
import Constants as chose

#much Refactoring needed 

CHEMIN_BD = 'synonymes.db'
FK_ON = 'PRAGMA foreign_keys = 1'

class BD:
    def __init__(self) -> None:
        self.chemin = CHEMIN_BD
    def __enter__(self):
        self.connecter()
        return self

    def __exit__ (self,exc_type,exc_value, exc_tb):
        #il manque juste curseur
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
        connexion = sqlite3.connect(self.chemin)
        curseur = connexion.cursor()
        curseur.execute(chose.CREATION_DATABASE)

    def deconnecter(self):
        self.curseur.close()
        self.connexion.close()

    # CHANGER POUR ÉCRIRE DANS LA BD POUR TABLE DICTIONNAIRE
    def inserer_dictionnaireBD(self, texte:list):
        dictionnaire = {}
        for mot in texte:
            if mot not in dictionnaire:
                dictionnaire[mot] = len(dictionnaire)


    # FONCTION POUR INSÉRER DANS TABLE SYNONYME
    def inserer_synonymeBD(idx_mot1:int, idx_mot2:int, fenetre:int, occ:int):
        pass

    
def main():
    with BD() as bd :

        #bd = BD()
        #conn, cur = bd.connecter()
        bd.creer_bd()
        print('fin')
 

if __name__ == '__main__' :
    main()