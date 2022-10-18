class Utils(object):
    def lire_fichier(fichier, encodage='utf-8'):
        f = open(fichier, 'r', encoding=encodage)
        s = f.read()
        s = s.lower()
        f.close()
        return s
    lire_fichier = staticmethod(lire_fichier)
    
