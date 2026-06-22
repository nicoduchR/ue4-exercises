# Séance 3 — Exercice de synthèse : la calculatrice testée

> Mettre en pratique fonctions, robustesse et tests.
> UE 4 · Management & Data Science

## Énoncé

| # | Étape | Description |
|:-:|-------|-------------|
| 1 | **4 fonctions** | Créer `addition`, `soustraction`, `multiplication` et `division`, chacune avec une docstring. |
| 2 | **Division sûre** | La division par zéro doit renvoyer un message clair, sans faire planter le programme. |
| 3 | **Tests** | Ajouter un jeu de tests avec `pytest`, couvrant tous les cas, dont la division par zéro. |

## Solution

Le fichier [`calculatrice.py`](calculatrice.py) contient les quatre fonctions demandées.

```python
def addition(a, b):
    """Retourne la somme de deux nombres."""
    return a + b
```

La division vérifie le cas interdit avant de calculer :

```python
def division(a, b):
    """Retourne le quotient de deux nombres ou un message si le diviseur vaut zéro."""
    if b == 0:
        return "Erreur : division par zéro impossible."
    return a / b
```

## Exécution

Lancer le petit exemple :

```bash
python seance-03/calculatrice.py
```

Lancer les tests :

```bash
pytest seance-03
```

## Rendu

- [`calculatrice.py`](calculatrice.py)
- [`test_calculatrice.py`](test_calculatrice.py)
