CREATION_TABLE_DICTIONNAIRE = '''

CREATE TABLE IF NOT EXISTS dictionnaire (
	id 					INTEGER 			PRIMARY KEY AUTOINCREMENT,
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
INSERT INTO dictionnaire(mot)
VALUES ('%s');
'''

AJOUTER_SYNONYME = '''
INSERT INTO synonyme(idx_mot1, idx_mot2, taille_fenetre ,nb_occurence)
VALUES (%d,%d,%d,%d);
'''

UPDATE_SYNONYME = '''
UPDATE synonyme
SET nb_occurence = %d
WHERE
    idx_mot1 = %d AND
	idx_mot2 = %d AND
	taille_fenetre = %d
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

SELECT_FROM = '''
SELECT %s FROM %s;'''

SELECT_FROM_WHERE = '''
SELECT %s FROM %s WHERE %s;
'''
