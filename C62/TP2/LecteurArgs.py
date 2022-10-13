import argparse
import os
import sys

class LecteurArgs:
    def __init__(self, description, liste_args) -> None:
        self.parser = argparse.ArgumentParser(description)
        self.liste_args = liste_args

    def set_option(self, var : str, act : str, metav : str, t : str, aide : str):
        if (var == '-e' and len(self.liste_args)==5) or (var == '-r' and len(self.liste_args) == 3):
            self.parser.add_argument(var, action=act, metavar=metav, type=t, help=aide)

        

 

