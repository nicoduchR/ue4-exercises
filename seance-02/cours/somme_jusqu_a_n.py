"""
Séance 2 — Exercice 2.3 : somme jusqu'à n

Énoncé : calculer 1 + 2 + … + n pour un n saisi par l'utilisateur.

Notions : input(), int(), boucle for, accumulateur (variable somme).
    Le principe de l'accumulateur : on part de 0, puis on ajoute chaque
    nombre un par un au fil de la boucle.

Bonus : la formule de Gauss n × (n + 1) / 2 donne le même résultat
        instantanément, sans boucle. On l'utilise ici pour vérifier.

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


# 1. La saisie : on demande la valeur de n.
n = demander_entier("Jusqu'à quel nombre veux-tu additionner ? n = ")

# 2. Le calcul : on accumule 1 + 2 + … + n dans la variable « somme ».
somme = 0
for nombre in range(1, n + 1):  # range(1, n+1) va de 1 jusqu'à n inclus.
    somme = somme + nombre

# 3. Le résultat.
print(f"1 + 2 + … + {n} = {somme}")

# Bonus : vérification avec la formule de Gauss (résultat identique).
verification = n * (n + 1) // 2
print(f"(vérification avec la formule de Gauss : {verification})")
