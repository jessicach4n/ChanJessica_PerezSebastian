import sqlite3

# EXEMPLE DE CODE BD ==========================================
CHEMINBD = 'emp_dep.db'
FOREIGN_KEYS = 'PRAGMA foreign_keys = 1'

CREER_DEPARTEMENT = '''
CREATE TABLE IF NOT EXISTS departement
(
    id INT PRIMARY KET NOT NULL,
    nom CHAR(15) UNIQUE NOT NULL
)
'''

DROP_DEPARTEMENT = 'DROP TABLE IF EXISTS departement'
INSERT_DEPARTEMENT = 'INSERT INTO departement(id, nom), VALUES(?,?)'
SELECT_DEPARTEMENT = 'SELECT * FROM departement'
DELETE_DEPARTEMENT = 'DELETE FROM departement WHERE nom = ?'


CREER_EMPLOYE = '''
CREATE TABLE IF NOT EXISTS employe
(
    id INT NOT NULL,
    id_departement INT NOT NULL,
    nom CHAR(15) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (id_departement) REFERENCES departement(id)
)
'''

DROP_EMPLOYE = 'DROP TABLE IF EXISTS employe'
INSERT_EMPLOYE = 'INSERT INTO employe(id, nom, id_departement), VALUES(?,?,?)'
SELECT_EMPLOYE = 'SELECT * FROM employe'
DELETE_EMPLOYE = 'DELETE FROM employe WHERE nom = ?'

def connecter(chemin_bd):
    connexion = sqlite3.connect(chemin_bd)
    curseur = connexion.cursor()
    curseur.execute(FOREIGN_KEYS)
    
    return connexion, curseur

def deconnecter(connexion, curseur): # Fermer la ressource
    curseur.close()
    connexion.close()
    
def creer_tables(curseur):
    curseur.execute(DROP_EMPLOYE) # Employe dépendant de département donc on l'enlève en premier
    curseur.execute(DROP_DEPARTEMENT) # Pas de dépendance

    curseur.execute(CREER_DEPARTEMENT)
    curseur.execute(CREER_EMPLOYE)
    
def inserer(curseur):
    curseur.execute(INSERT_DEPARTEMENT, (1, 'Informatique'))
    curseur.execute(INSERT_EMPLOYE, (1000, 'Marcel', 1))
    curseur.execute(INSERT_EMPLOYE, (2000, 'Michelle', 1))
    curseur.execute(INSERT_EMPLOYE, (3000, 'Richard', 1))
    curseur.execute(INSERT_EMPLOYE, (4000, 'Toto', 1))
    
    # Quand on communique avec la BD, c'est long. Solution pour rendre plus facile :


def afficher(curseur):
    print('**********DEPARTEMENT************')
    curseur.execute(SELECT_DEPARTEMENT)
    for rangee in curseur.fetchall():
        print(rangee)
    
    print('**********DEPARTEMENT************')
    curseur.execute(SELECT_EMPLOYE)
    for rangee in curseur.fetchall():
        print(rangee)

def main():
    
    conn, cur = connecter(CHEMINBD)
    
    creer_tables(cur) # Mettre en commentaire si la base de données et les tables sont déjà créés
    inserer(cur)
    conn.commit() # Faut faire un commit après un insert
    afficher(cur)
    cur.execute(DELETE_EMPLOYE, ('Toto',)) # Doit être un tuple, donc ajouter virgule si juste une valeur
    conn.commit() # À chaque manipulation des tables, faut faire un commit, sinon les changements ne sont pas appliqués sur la BD
    
    # cur.execute(DELETE_DEPARTEMENT, ('Informatique'),) # Ne peut pas être supprimer à cause des dépendances
    
    employes = [(5000, 'JMD', 1), (6000, 'JCD', 1)]
    cur.executemany(INSERT_EMPLOYE, (employes,)) # Faire plusieurs insert en une seule exécution
    
    deconnecter(conn, cur)
    
    return 0
    
# =============================================================
     
if __name__ == '__main__':
    quit(main())