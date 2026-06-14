"""
Séance 2 — Exercice 2.1 : pair ou impair

Énoncé : demander un nombre et dire s'il est pair ou impair.
Indice : l'opérateur modulo « % » donne le reste d'une division.
    - un nombre est PAIR  si son reste dans la division par 2 vaut 0 ;
    - un nombre est IMPAIR sinon (le reste vaut 1).

Notions : input(), int(), opérateur modulo (%), condition if / else.

UE 4 · Management & Data Science
"""


def demander_entier(message):
    """Lit un entier au clavier, en redemandant tant que la saisie est invalide."""
    while True:
        saisie = input(message)
        try:
            return int(saisie)
        except ValueError:
            print("  Ce n'est pas un nombre entier, réessaie.")


# 1. La saisie : on demande un nombre entier à l'utilisateur.
nombre = demander_entier("Entre un nombre entier : ")

# 2. Le test : reste de la division par 2 (0 = pair, sinon impair).
if nombre % 2 == 0:
    print(f"{nombre} est un nombre pair.")
else:
    print(f"{nombre} est un nombre impair.")
