from Arguments import Arguments

def main():
    try:
        a = Arguments()
        a.traiter_arguments()
    except:
        return 1
    return 0
          
if __name__ == '__main__':
    quit(main())
    
    
    
