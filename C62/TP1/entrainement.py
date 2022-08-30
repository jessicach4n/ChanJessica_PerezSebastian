class Entrainement:
    def __init__(self):
        pass
    
    def read_file(self, fichier):
        f = open(fichier, "r")
        print(f.read())
        
if __name__ == '__main__':
    e = Entrainement()
    e.read_file("./textes/test.txt")