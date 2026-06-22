"""
Séance 3 — Exercice de synthèse : la calculatrice testée

Objectif :
    - écrire quatre fonctions de calcul ;
    - documenter chaque fonction avec une docstring ;
    - gérer la division par zéro sans faire planter le programme.

UE 4 · Management & Data Science
"""


def addition(a, b):
    """Retourne la somme de deux nombres."""
    return a + b


def soustraction(a, b):
    """Retourne la différence entre deux nombres."""
    return a - b


def multiplication(a, b):
    """Retourne le produit de deux nombres."""
    return a * b


def division(a, b):
    """Retourne le quotient de deux nombres ou un message si le diviseur vaut zéro."""
    if b == 0:
        return "Erreur : division par zéro impossible."

    return a / b


if __name__ == "__main__":
    print("Addition :", addition(10, 5))
    print("Soustraction :", soustraction(10, 5))
    print("Multiplication :", multiplication(10, 5))
    print("Division :", division(10, 5))
    print("Division par zéro :", division(10, 0))
