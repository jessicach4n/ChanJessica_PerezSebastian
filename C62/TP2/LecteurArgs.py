import argparse
import os
import sys

class LecteurArgs:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description='User input')
        parser.add_argument('-e', action='store_true', help='Executer un entrainement')
        parser.add_argument('-r', action='store_true', help='Executer une recherche')
        parser.add_argument('-b', action='store_true', help='Recreer la base de donnees')

        parser.add_argument('-t', nargs='?', type=int, help='Specifier la taille de fenetre')
        parser.add_argument('--enc', nargs='?', help="Specifier l'encodage")
        parser.add_argument('--chemin', nargs='?', help='Specifier le chemin du fichier texte')
        
        self.args = parser.parse_args()

    def traiter_arguments(self):
        if self.args.e:
            if self.args.t is None or self.args.enc is None or self.args.chemin is None:
                return 'Erreur : Entrainement besoin de trois arguments'
            elif self.args.t <= 0 or self.args.enc not in ['utf-8']:
                return 'Erreur : Mauvais arguments'
            return 'Entrainement'
        elif self.args.r:
            if self.args.t is None:
                return 'Erreur : Recherche besoin argument taille -t'
            return 'Recherche'
        elif self.args.b:
            return 'Database'
        

 

