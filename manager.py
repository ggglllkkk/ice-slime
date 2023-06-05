#Récupérer les inputs
def getKeys():
    dico={}
    with open("data/storedData/keys.csv", "r", encoding="utf-8") as file:
        for k in file.readlines():
            a=k.rstrip().split(";")
            dico[a[0]] = [int(n) for n in a[1:]]
    return dico

#Récupérer les textes des langues
def getTexts():
    dico={}
    with open("data/storedData/texts.csv", "r", encoding="utf-8") as file:
        for k in file.readlines():
            a=k.rstrip().split(";")
            dico[a[0]] = a[1:]
    return dico