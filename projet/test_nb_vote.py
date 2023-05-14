from traitement import nb_vote

# la première liste contient tous les indice de projet qui ont été voté ainsi que le nombre de chacun des votes et la deuxième 
# tous les indices de projets de la page. La deuxième liste est donc forcément de taille supérieur ou égale a la première.

def test_base_1(): # test du cas de base quand les deux liste sont vides 
    assert nb_vote([],[]) == []

def test_base_2(): # test aucun des projets conernés n'a de vote
    assert nb_vote([],[(1,),(2,),(3,),(4,)]) == [(0,1),(0,2),(0,3),(0,4)]

def test_base_3(): # seul un test a été voté au moins une fois
    assert nb_vote([(2,3)],[(1,),(2,),(3,),(4,)]) == [(0,1),(0,2),(2,3),(0,4)]

def test_base_4(): # tous on été voté
    assert nb_vote([(16,1),(2,2),(7,3),(9,4)],[(1,),(2,),(3,),(4,)]) == [(16,1),(2,2),(7,3),(9,4)]

def test_base_5(): # le premier n'a pas été voté
    assert nb_vote([(2,2),(4,4)],[(1,),(2,),(3,),(4,)]) == [(0,1),(2,2),(0,3),(4,4)]

def test_base_6(): # plusieurs projet en fin de liste non pas été voté
    assert nb_vote([(2,2),(4,4)],[(2,),(4,),(5,),(6,),(7,),(8,)]) == [(2,2),(4,4),(0,5),(0,6),(0,7),(0,8)]

def test_base_7(): # seul le dernier a été voté
    assert nb_vote([(1,9)],[(1,),(3,),(4,),(5,),(8,),(9,)]) == [(0,1),(0,3),(0,4),(0,5),(0,8),(1,9)]