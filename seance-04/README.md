# Séance 4 — Exercice de synthèse : historique du taux EUR → USD

> Combiner API, fichier CSV et gestion d'erreurs.
> UE 4 · Management & Data Science

## Énoncé

| # | Étape | Description |
|:-:|-------|-------------|
| 1 | **Récupérer** | Le taux EUR/USD des 30 derniers jours via une API. |
| 2 | **Stocker & analyser** | Écrire un CSV, le relire, calculer moyenne, min, max. |
| 3 | **Robustesse** | Afficher les dates du min/max et gérer l'absence de réseau. |

**À rendre :** un programme qui produit le CSV + un mini-rapport texte.

## Solution

Le fichier [`historique_taux_eur_usd.py`](historique_taux_eur_usd.py) enchaîne les
trois étapes. Il n'utilise que la **bibliothèque standard** (`urllib`, `json`,
`csv`, `datetime`, `statistics`) : aucun package à installer.

### 1. Récupérer

L'historique est demandé en une seule requête grâce à l'endpoint « plage de
dates » de l'API [Frankfurter](https://www.frankfurter.app/) (taux de référence
de la BCE) :

```
https://api.frankfurter.app/2026-05-29..2026-06-29?from=EUR&to=USD
```

La BCE ne cote pas les week-ends : on obtient donc les **jours ouvrés** de la
période (≈ 22 relevés pour 30 jours calendaires).

### 2. Stocker & analyser

Le programme **écrit** le CSV puis le **relit** (preuve qu'il est exploitable),
avant de calculer la moyenne, le minimum et le maximum :

```python
def analyser(historique):
    """Calcule moyenne, minimum et maximum (avec leurs dates) de l'historique."""
    taux = [valeur for _, valeur in historique]
    date_min, taux_min = min(historique, key=lambda couple: couple[1])
    date_max, taux_max = max(historique, key=lambda couple: couple[1])
    ...
```

### 3. Robustesse

- Les **dates** du minimum et du maximum sont conservées (et non seulement les
  valeurs) puis affichées dans le rapport.
- Si l'API est injoignable (pas de réseau, panne, *timeout*), le programme
  **ne plante pas** : il bascule sur un jeu de données de secours déterministe
  et l'indique clairement dans la source (`hors ligne (données de secours)`).

## Exécution

```bash
python seance-04/historique_taux_eur_usd.py
```

Le programme crée deux fichiers à côté du script :

| Fichier | Contenu |
|---------|---------|
| [`taux_eur_usd_30j.csv`](taux_eur_usd_30j.csv) | Une ligne par jour ouvré : `date,taux_eur_usd`. |
| [`rapport.txt`](rapport.txt) | Le mini-rapport : période, moyenne, min/max et leurs dates. |

### Exemple de rapport produit

```
Rapport — historique du taux EUR -> USD (30 derniers jours)
==========================================================
Source des donnees : Frankfurter / BCE
Periode analysee   : du 2026-05-29 au 2026-06-29
Nombre de releves  : 22 (jours ouvres)

Taux moyen   : 1.1529 USD
Taux minimum : 1.1340 USD  (le 2026-06-24)
Taux maximum : 1.1649 USD  (le 2026-06-02)
Amplitude    : 0.0309 USD
```

## Rendu

- [`historique_taux_eur_usd.py`](historique_taux_eur_usd.py)
- [`taux_eur_usd_30j.csv`](taux_eur_usd_30j.csv) *(généré)*
- [`rapport.txt`](rapport.txt) *(généré)*
