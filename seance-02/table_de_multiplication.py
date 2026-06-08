"""
Séance 2 — Exercice 2.2 : table de multiplication

Énoncé : afficher la table de 7, de 7×1 à 7×10, avec une boucle « for ».

Notions : boucle for, range(), f-string.
    - range(1, 11) parcourt les entiers de 1 à 10 (la borne 11 est exclue) ;
    - à chaque tour, la variable i prend la valeur suivante.

UE 4 · Management & Data Science
"""

TABLE = 7  # on peut changer ce nombre pour afficher une autre table.

print(f"Table de multiplication de {TABLE} :")

# La boucle for répète l'affichage pour i allant de 1 à 10.
for i in range(1, 11):
    resultat = TABLE * i
    print(f"{TABLE} x {i:2d} = {resultat}")
