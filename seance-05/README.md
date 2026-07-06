# Séance 5 — Contrôle continu : analyse du taux EUR/USD

> Le projet noté qui mobilise tout le cours.
> UE 4 · Management & Data Science

## Énoncé

| # | Étape | Description |
|:-:|-------|-------------|
| 1 | **Télécharger** | Taux EUR/USD des 2 dernières années → `eur_usd.csv`. |
| 2 | **Préparer** | Charger dans Pandas, index temporel trié, traiter les jours manquants. |
| 3 | **Explorer** | Rendement journalier en %, statistiques descriptives. |
| 4 | **Prévoir** | Régression linéaire pour prédire le lendemain, calculer le RMSE. |

**Livrables :** `taux_change_analysis.py` (ou `.ipynb`) + graphiques + commentaire — par mail.

## Solution

Le fichier [`taux_change_analysis.py`](taux_change_analysis.py) enchaîne les
quatre étapes. Contrairement aux séances précédentes, il s'appuie sur les
bibliothèques du cours de data science :

```bash
pip install pandas matplotlib scikit-learn
```

### 1. Télécharger

Deux ans d'historique sont demandés en une seule requête à l'API
[Frankfurter](https://www.frankfurter.app/) (taux de référence de la BCE),
comme à la séance 04, puis écrits dans [`eur_usd.csv`](eur_usd.csv) :

```
https://api.frankfurter.app/2024-07-05..2026-07-06?from=EUR&to=USD
```

Si l'API est injoignable, le programme bascule sur un jeu de données de
secours déterministe (même mécanisme qu'à la séance 04).

### 2. Préparer

```python
df = pd.read_csv(chemin, parse_dates=["date"], index_col="date")
df = df.sort_index()          # index temporel trié
df = df.asfreq("D")           # tous les jours calendaires → NaN les jours non cotés
df["taux_eur_usd"] = df["taux_eur_usd"].ffill()   # propagation du dernier fixing
```

La BCE ne cote ni les week-ends ni les jours fériés : la réindexation
journalière fait apparaître ces trous en `NaN`, comblés par **propagation du
dernier taux connu** (`ffill`) — le week-end, le taux applicable reste celui
du dernier fixing.

### 3. Explorer

Le rendement journalier est la variation relative d'un jour à l'autre :

```python
df["rendement_pct"] = df["taux_eur_usd"].pct_change() * 100
df["rendement_pct"].describe()
```

Trois graphiques sont produits dans [`graphiques/`](graphiques/) : l'évolution
du taux (avec moyenne mobile 30 j), la série et la distribution des rendements,
et la comparaison réel/prédit de l'étape 4.

### 4. Prévoir

On prédit le taux du **lendemain** à partir du taux du **jour** :

```python
X = couples[["taux_du_jour"]]      # taux en t
y = couples["taux_du_lendemain"]   # taux en t+1
```

Le découpage entraînement/test est **chronologique** (80 % les plus anciens /
20 % les plus récents, sans mélange — on ne s'entraîne jamais sur le futur).
Le RMSE de la régression est comparé à celui d'un modèle naïf
« demain = aujourd'hui ».

## Exécution

```bash
python seance-05/taux_change_analysis.py
```

Le programme crée à côté du script :

| Fichier | Contenu |
|---------|---------|
| [`eur_usd.csv`](eur_usd.csv) | Une ligne par jour coté : `date,taux_eur_usd`. |
| [`commentaire.txt`](commentaire.txt) | Chiffres clés + interprétation (le commentaire du rendu). |
| [`graphiques/01_taux_eur_usd.png`](graphiques/01_taux_eur_usd.png) | Taux sur 2 ans + moyenne mobile 30 j. |
| [`graphiques/02_rendements_journaliers.png`](graphiques/02_rendements_journaliers.png) | Série + histogramme des rendements. |
| [`graphiques/03_prevision_regression.png`](graphiques/03_prevision_regression.png) | Réel vs prédit sur la période de test. |

### Résultats obtenus (exécution du 2026-07-06)

```
Modele : taux_demain = 0.9974 x taux_du_jour +0.0031
RMSE (regression)                 : 0.00374 USD
RMSE (naif, demain = aujourd'hui) : 0.00373 USD
Prevision pour demain             : 1.1416 USD
```

**Ce qu'il faut en retenir** : la pente vaut ≈ 1 et l'ordonnée à l'origine ≈ 0,
donc la meilleure prédiction linéaire du taux de demain est… presque le taux
d'aujourd'hui. La régression ne bat pas le modèle naïf : un taux de change se
comporte quasiment comme une **marche aléatoire**, l'information passée est
déjà dans le prix. L'intérêt du modèle n'est pas de « battre le marché » mais
de **quantifier l'incertitude** : l'erreur type (~0.004 USD) donne l'ordre de
grandeur du mouvement attendu d'un jour à l'autre.

Autre point d'attention : le pic de rendements à exactement 0 % dans
l'histogramme est un **artefact du `ffill`** (les jours comblés ne bougent pas,
par construction) — il faut le savoir avant d'interpréter les statistiques.

## Rendu

- [`taux_change_analysis.py`](taux_change_analysis.py)
- [`eur_usd.csv`](eur_usd.csv) *(généré)*
- [`commentaire.txt`](commentaire.txt) *(généré)*
- [`graphiques/`](graphiques/) *(générés)*
