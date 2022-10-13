class Utils(object):
    def lire_fichier(fichier, encodage='utf-8'):
        f = open(fichier, 'r', encoding=encodage)
        s = f.read()
        s = s.lower()
        f.close()
        return s
    lire_fichier = staticmethod(lire_fichier)
    
    def creer_dict_mots(texte):
        dictionnaire = {}
        for mot in texte:
            if mot not in dictionnaire:
                dictionnaire[mot] = len(dictionnaire)
        return dictionnaire
    creer_dict_mots = staticmethod(creer_dict_mots)