from traitement import fusion_paire_derec


def test_base(): #test liste vide
    assert fusion_paire_derec([], []) == []

def test_base_2(): #test liste avec un seul élément dans la liste de gauche
    assert fusion_paire_derec([(1,1)], []) == [(1,1)]

def test_base_3(): #test liste avec un seul élément dans la liste de droite
    assert fusion_paire_derec([], [(1,1)]) == [(1,1)]

def test_base_4(): #test avec deux liste à un seul élément
    assert fusion_paire_derec([(1,1)], [(1,1)]) == [(1,1), (1,1)]

def test_simple_1(): #test avec deux listes "simples"
    assert fusion_paire_derec([(1, 2), (2, 1), (5, 4)], [(1, 1), (4, 2), (6, 0)]) == [(1, 1), (1, 2), (2, 1), (4, 2), (5, 4), (6, 0)]

def test_simple_2(): #test avec deux listes "simples"
    assert fusion_paire_derec([(1, 1), (1, 3), (2, 1)], [(2, 1), (2, 2), (2, 1)]) == [(1, 1), (1, 3), (2, 1), (2, 2), (2, 1), (2, 1)]