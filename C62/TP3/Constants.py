QUITTER = 'q'

MESS = f'''
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez "{QUITTER}" pour quitter.

'''

CREATION_TABLE_DICTIONNAIRE = '''

CREATE TABLE IF NOT EXISTS dictionnaire (
	id 					INTEGER 			PRIMARY KEY,
	mot		 			VARCHAR ( 100 ) 	NOT NULL
);

''' 
CREATION_TABLE_SYNONIME = '''
CREATE TABLE IF NOT EXISTS synonyme (
	idx_mot1		 			INT 	NOT NULL,
  	idx_mot2		 			INT  	NOT NULL,
  	taille_fenetre		 		INT  	NOT NULL,
  	nb_occurence				INT		NOT NULL,
  
    PRIMARY KEY ( idx_mot1, idx_mot2, taille_fenetre),
	
  	CONSTRAINT fk_idx1_mot
      FOREIGN KEY(idx_mot1) 
	  REFERENCES dictionnaire(id),

  	CONSTRAINT fk_idx2_mot
      FOREIGN KEY(idx_mot2) 
	  REFERENCES dictionnaire(id)
);
'''
AJOUTER_MOT_DICTIONNAIRE = '''
INSERT INTO dictionnaire(id, mot)
VALUES (?,?);
'''

AJOUTER_SYNONYME = '''
INSERT INTO synonyme(idx_mot1, idx_mot2, taille_fenetre ,nb_occurence)
VALUES (?,?,?,?);
'''

UPDATE_SYNONYME = '''
UPDATE synonyme
SET nb_occurence = ?
WHERE
    idx_mot1 = ? AND
	idx_mot2 = ? AND
	taille_fenetre = ?
'''

DROP_TABLE_SYNONYME = '''
DROP TABLE IF EXISTS synonyme;
'''

DROP_TABLE_DICTIONNAIRE = '''
DROP TABLE IF EXISTS dictionnaire;
'''

SELECT_FROM_DICTIONNAIRE = '''
SELECT * FROM dictionnaire;
'''

SELECT_FROM_SYNONYME = '''
SELECT * FROM synonyme;
'''

SELECT_FROM_SYNONYME_WHERE = '''
SELECT idx_mot1, idx_mot2, nb_occurence FROM synonyme WHERE ?;
'''
