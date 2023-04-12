from Othello1 import *

def test_creer_partie():
    assert creer_partie(4)
    assert creer_partie(6)
    assert creer_partie(8)

def test_saisie_valide():
    p=creer_partie(4)
    assert saisie_valide(p, "a1")
    assert saisie_valide(p, "b4")
    assert not saisie_valide(p,"c6")
    p=creer_partie(6)
    assert saisie_valide(p, "a1")
    assert saisie_valide(p, "b4")
    assert not saisie_valide(p,"c8")
    p=creer_partie(8)
    assert saisie_valide(p, "a1")
    assert saisie_valide(p, "b4")
    assert not saisie_valide(p,"c9")

test_saisie_valide()
test_saisie_valide()
