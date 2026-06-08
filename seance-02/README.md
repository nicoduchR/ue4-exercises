# Séance 2 — Exercices guidés : conditions & boucles

> Exercices guidés (1/2) — découverte des **conditions** et des **boucles**.
> UE 4 · Management & Data Science

## Énoncé

| # | Exercice | Description |
|:-:|----------|-------------|
| 2.1 | **Pair ou impair** | Demander un nombre, dire s'il est pair ou impair (indice : `% 2`). |
| 2.2 | **Table de multiplication** | Afficher la table de 7, de 7×1 à 7×10, avec une boucle `for`. |
| 2.3 | **Somme jusqu'à n** | Calculer 1 + 2 + … + n pour un `n` saisi par l'utilisateur. |

> Conseil de l'énoncé : *écrivez l'algorithme en français avant de coder.*

## Solutions

### 2.1 — Pair ou impair · [`pair_ou_impair.py`](pair_ou_impair.py)

Le **modulo** `%` donne le reste d'une division. Un nombre est pair quand son
reste dans la division par 2 vaut 0, impair sinon.

```python
nombre = int(input("Entre un nombre entier : "))

if nombre % 2 == 0:
    print(f"{nombre} est un nombre pair.")
else:
    print(f"{nombre} est un nombre impair.")
```

### 2.2 — Table de multiplication · [`table_de_multiplication.py`](table_de_multiplication.py)

La boucle `for` associée à `range(1, 11)` répète l'opération pour `i` allant de
**1 à 10** (la borne 11 est exclue).

```python
TABLE = 7
for i in range(1, 11):
    print(f"{TABLE} x {i} = {TABLE * i}")
```

### 2.3 — Somme jusqu'à n · [`somme_jusqu_a_n.py`](somme_jusqu_a_n.py)

On utilise un **accumulateur** : la variable `somme` part de 0 et on lui ajoute
chaque nombre, un par un, au fil de la boucle.

```python
n = int(input("n = "))

somme = 0
for nombre in range(1, n + 1):   # de 1 jusqu'à n inclus
    somme = somme + nombre

print(f"1 + 2 + … + {n} = {somme}")
```

> **Bonus** : la formule de Gauss `n * (n + 1) // 2` donne le même résultat
> instantanément, sans boucle. Le script l'affiche pour vérifier.

## Notions abordées

- **Condition `if / else`** : exécuter un bloc *ou* un autre selon un test.
- **Opérateur modulo `%`** : le reste d'une division entière (clé du test pair/impair).
- **Boucle `for` + `range()`** : répéter une action un nombre connu de fois.
- **Accumulateur** : une variable que l'on fait grossir tour après tour.
- **`int()`** : convertir la saisie (toujours une chaîne) en nombre entier.

> **Petit plus** — robustesse : `pair_ou_impair.py` et `somme_jusqu_a_n.py`
> redemandent la valeur tant que la saisie n'est pas un entier valide
> (`try / except ValueError`), pour éviter que le programme plante.

## Exécution

```bash
python seance-02/pair_ou_impair.py
python seance-02/table_de_multiplication.py
python seance-02/somme_jusqu_a_n.py
```

### Exemples

```
Entre un nombre entier : 17
17 est un nombre impair.
```

```
Table de multiplication de 7 :
7 x  1 = 7
7 x  2 = 14
...
7 x 10 = 70
```

```
Jusqu'à quel nombre veux-tu additionner ? n = 100
1 + 2 + … + 100 = 5050
(vérification avec la formule de Gauss : 5050)
```

## Rendu

- **Format** : un fichier `.py` ou `.ipynb` par exercice.
- **Destinataire** : voir le [README principal](../README.md) du dépôt.
