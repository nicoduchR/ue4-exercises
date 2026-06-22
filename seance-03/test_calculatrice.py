from calculatrice import addition, division, multiplication, soustraction


def test_addition():
    assert addition(2, 3) == 5
    assert addition(-2, 3) == 1
    assert addition(2.5, 1.5) == 4.0


def test_soustraction():
    assert soustraction(10, 4) == 6
    assert soustraction(4, 10) == -6
    assert soustraction(2.5, 0.5) == 2.0


def test_multiplication():
    assert multiplication(3, 4) == 12
    assert multiplication(-3, 4) == -12
    assert multiplication(2.5, 2) == 5.0


def test_division():
    assert division(10, 2) == 5
    assert division(-9, 3) == -3
    assert division(5, 2) == 2.5


def test_division_par_zero():
    assert division(10, 0) == "Erreur : division par zéro impossible."
