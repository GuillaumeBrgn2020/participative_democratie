from traitement import calculpola

def test_positif(): # un commentaire positif doit etre positif
    assert calculpola("Tu es très beau") >= 0 

def test_negatif(): # un commentaire négatif doit être négatif
    assert calculpola("Tu es très moche") <= 0     

def test_vide(): # un commentaire vide ne vaut rien (mais ne peut pas être posté)
    assert calculpola("") == 0

def test_liste(): # une liste ne vaut rien
    assert calculpola([1,2,3]) == 0 

def test_integer(): # un entier ne vaut rien
    assert calculpola(42) == 0

def test_maximum_character(): # si on dépasse le nombre de caractères permis par le site, la fonction marche quand même
    L = []
    for i in range(0,3334):
        L.append(1)
    L = str(L) # len(L) vaut 10 002 (3 334 * 3 car on transforme une liste en str)

    assert type(calculpola(L)) == int 

def test_negation(): # une négation inverse la polarité d'un mot
    assert calculpola("Tu n'es pas beau") == -calculpola('Tu es beau')

def test_insistance(): # un point d'exclamation marque un sentiment insisté, une note supérieure est donc accordée au mot
    assert calculpola("Tu es beau !") >= calculpola("Tu es beau")

def test_insistance2():
    assert calculpola("Tu es très beau") >= calculpola("Tu es beau")
