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
  
  PRIMARY KEY ( idx_mot1, idx_mot2, taille_fenetre)
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

#Pour Tester La bd dans le terminal 
SELECT_ALL_FROM_TABLE_DICTIONNAIRE= '''
SELECT * FROM dictionnaire;
'''

SELECT_ALL_FROM_TABLE_SYNONYMES= '''
SELECT * FROM synonyme;
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

SELECT_COUNT_SYNONYME = '''
SELECT DISTINCT COUNT(idx_mot1) FROM synonyme WHERE taille_fenetre = ?;
'''
