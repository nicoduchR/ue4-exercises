"""
Séance 2 — Exercice de synthèse : FizzBuzz

L'exercice de recrutement le plus classique. Il combine les deux notions
de la séance : la boucle « for » (parcourir) et les conditions « if / elif / else ».

Énoncé :
    1. Parcourir   — boucler sur les entiers de 1 à 100.
    2. Les règles  — multiple de 3       → « Fizz »
                     multiple de 5       → « Buzz »
                     multiple de 3 ET 5  → « FizzBuzz »
    3. Sinon       — afficher simplement le nombre.

Le piège : il faut tester le cas « 3 ET 5 » EN PREMIER. Sinon, un nombre
comme 15 (multiple de 3 et de 5) serait attrapé par le test « multiple de 3 »
et afficherait « Fizz » au lieu de « FizzBuzz ».
    Rappel : un multiple de 3 et de 5 est un multiple de 15.

Notions : boucle for, range(), opérateur modulo (%), if / elif / else.

UE 4 · Management & Data Science
"""


# 1. On parcourt les entiers de 1 à 100 (range(1, 101) : la borne 101 est exclue).
for nombre in range(1, 101):

    # 2. Les règles, du cas le plus précis au plus général.
    if nombre % 15 == 0:          # multiple de 3 ET de 5 → on teste 15 d'abord.
        print("FizzBuzz")
    elif nombre % 3 == 0:         # multiple de 3 seulement.
        print("Fizz")
    elif nombre % 5 == 0:         # multiple de 5 seulement.
        print("Buzz")
    else:                         # 3. Sinon : aucun multiple, on affiche le nombre.
        print(nombre)
