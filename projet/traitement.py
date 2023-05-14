#Fichier contenant toutes les fonctions de traitement des données


def fusion_paire_aux(l1: list, l2: list, acc: list) -> list: # n'est plus utilisée car on a implémenté la version dérécursivé
    """
    fusion auxilière de deux listes de tuples à deux éléments triées sur le premier élément du tuple comme comparateur
    Elle est récursive terminale
    """
    if l1 == []: #cas de base
        return acc + l2
    elif l2 == []: #cas de base
        return acc + l1
    else:
        el11, el12 = l1[0] #séparation du tuple
        el21, el22 = l2[0] #séparation du tuple
        if el11 < el21: # comparaison selon le premier élément des tuples
            return fusion_paire_aux(l1[1:], l2, acc + [(el11, el12)]) # appel récursif terminal
        else:
            return fusion_paire_aux(l1, l2[1:], acc + [(el21, el22)]) # appel récursif terminal


def fusion_paire(l1: list,l2: list) -> list: # n'est plus utilisée car on a implémenté la version dérécursivé
    """
    fusion auxilière de deux listes de tuples à deux éléments triées sur le premier élément du tuple comme comparateur
    """
    return fusion_paire_aux(l1, l2, [])


def fusion_paire_derec(l1: list, l2:list) -> list:
    """
    fonction fusion_paire dérécursivé
    """
    c1 = l1[:] #copie des listes
    c2 = l2[:]
    acc = [] # création de la variable résultat
    while len(c1) != 0 and len(c2) != 0: #vérification du cas d'arrêt
        el11, el12 = c1[0] #séparation des tuples
        el21, el22 = c2[0]
        if el11 < el21: #comparaison des premières valeurs des tuples
            el = c1.pop(0) #on retire le premier tuple
            acc = acc + [el]
        else:
            el = c2.pop(0) #on retire le premier tuple
            acc = acc + [el]

    if len(c1) ==0: # vérification pour savoir quel cas de base on applique
        return acc + c2
    else:
        return acc + c1
        


def tri_fusion_paire(l: list) -> list:
    """
    tri fusion avec une liste de tuple de deux éléments avec le premier élément du tuple comme comparateur
    """
    if type(l) != list:
        return []
    if len(l) <= 1: # cas d'une liste vide ou à un seul tuple
        return l
    else:
        return fusion_paire_derec(tri_fusion_paire(l[0:len(l)//2]), tri_fusion_paire(l[len(l)//2:])) # cas général




def creation():
    """
    Création des listes pour le dico
    """
    mots = []
    polarites = []
    ftest = open("Les_mots.txt","r") #ouverture du fichier en mode lecture
    lines = ftest.readlines()
    nombredemot = len(lines)
    for i in range(0,nombredemot-1):
        line = lines[i].splitlines()
        tout = line[0].rsplit('\t')

        if len(tout) !=  2:
            tout = list(filter(None, tout)) #on enlève les caractères vides ds la liste
            tout = tout[0].rsplit(' ')
        tout = list(filter(None, tout)) #on enlève les caractères vides ds la liste

        mots.append(tout[0].lower())
        polarites.append(int(tout[1]))

    new_Mots = []
    new_Pola = []

    for i in range(len(mots)) : #on enlève les doublons des listes pour dico
        if mots[i] not in new_Mots: 
            new_Mots.append(mots[i])
            new_Pola.append(polarites[i]) 

    mots = new_Mots
    polarites = new_Pola
    liste_ponctuation = [',', '.', "'", '"', ';', ':', '(', ')', '[', ']', '...', '-', '_', '/', '?', '{', '}', '=', '+', '^']
    liste_insistance = ["très", "trop", "tres", "vraiment", "vachement", "carrément", "carrement", "enormement", "énormément", "énormement", "totalement"]
    dico = dict(zip(mots,polarites)) #c'est le dico 

    return mots, polarites, liste_insistance, liste_ponctuation, dico

def calculpola(phrase: str) -> float: #calcul de polarité
    """
    Calcul de la polarité moyenne d'une phrase
    """
    mots, polarites, liste_insistance, liste_ponctuation, dico = creation()
    if phrase == "": # cas impossible, un commentaire ne peut pas être vide
        return 0
    if type(phrase) != str: # met tout en str pour éviter toute sorte de problème
        return 0

    phrase = phrase.replace("'", " ")
    phrase = phrase.lower() #on met en minuscule
    phrase = phrase.splitlines() #on récupère une liste des mots un a un 
    for j in liste_ponctuation : # on enlève ici les ponctuations dérangeantes 
        phrase = phrase[0].rsplit(j) 
        phrase = "".join(phrase)
        phrase = phrase.splitlines() 
    phrase = phrase[0].rsplit(' ') 
    phrase = list(filter(None, phrase)) #on enlève les caractères vides dans la liste

    pol = 0 
    a = 0 #augmente de 1 chaque fois qu'on mot est reconnu
    absent, present =[] ,[] # permet de voir les mots présents et absents de la phrase relativement au dictionnaire
    
    for i in range(len(phrase)):
        if phrase[i] in dico:
            present.append(phrase[i]) #stocke les mots présents 
            a += 1 # compte le nombre de mot présent, correspont a len(present)
            if phrase[i-1] == "pas" and i >= 1 :
                pol = pol - dico[phrase[i]]
                if  i < len(phrase)-1 and phrase[i+1] == "!":
                    pol -= 1
            elif len(phrase) > 1 and phrase[i-2] == "pas" and i >= 2 : #Si y a une négation sur le mot avant, style "cool" et "pas cool" ou "pas très cool", modifie la polarité par son opposé
                pol = pol - dico[phrase[i]]
                if  i < len(phrase)-1 and phrase[i+1] == "!": 
                    pol -= 1
                if phrase[i-1] in liste_insistance: # insister rajoute ou enlève des points
                    pol -= 1
            
            else :
                pol = pol + dico[phrase[i]]
                if  i < len(phrase)-1 and phrase[i+1] == "!": #l'ajout d'un '!' augmente la polarité de un, ou la diminue pour des phrases négative
                    if dico[phrase[i]] > 0:
                        pol +=1
                    elif dico[phrase[i]] < 0:
                        pol -=1
                if i > 1 and (phrase[i-1] in liste_insistance) : # insister rajoute ou enlève des points
                    if dico[phrase[i]] > 0:
                        pol +=1
                    elif dico[phrase[i]] < 0: 
                        pol -=1

        else :
            absent.append(phrase[i])
    if a == 0:
        return 0

    return pol/a



def nb_vote(l1: list,l2: list) -> list:
    """
    prend en argument une liste de tuple l1 contenant tous les indices et le nombre de vote pour chacun des projets qui ont un vote
    et l2 la liste des tuples (i,) avec i tous les indices des projets concernés
    renvoie une liste de tuple avec en premier élement le nombre de vote et 0 si le projet n'a pas de vote
    et en deuxième l'id du projet à partir d'une liste 
    """
    pas1=0;pas2=0  ## initialise les indices et la liste qui contiendra les résultats
    res = []
    while pas1 <len(l1) and pas2 <len(l2) : ## les indices étant trié dans l'ordre avec l1 une liste plus petite que l2
        if l1[pas1][1] == l2[pas2][0]:      ## on regarde si l'indice rang pas1 de l1 est le même que l'indice rang pas2 de l2 
            res.append(l1[pas1])            ## si oui on ajoute le résultat à la liste et on incrémente les deux indices
            pas1 += 1
            pas2 += 1    
        else:
            res.append((0, l2[pas2][0]))    ## sinon l'indice pas2 de l2 n'a pas de commentaire donc on ajoute 0 a la liste
            pas2 += 1                       ## et on incrémente pas2 
    while pas2 <len(l2):                    ## comme l1 est plus petit que l2 si jamais il y a beaucoup de projet non-commenté
        res.append((0, l2[pas2][0]))        ## on complète le résultat ici, si l1 et l2 on la même longueur alors tout les projets ont été commenté
        pas2 += 1
    return res