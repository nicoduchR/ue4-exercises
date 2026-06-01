# Séance 1 — Exercice de synthèse : convertisseur € → $

> Le « plus gros » exercice de la séance — **à rendre**.
> UE 4 · Management & Data Science

## Énoncé

| # | Étape | Description |
|:-:|-------|-------------|
| 1 | **Le taux** | Définir un taux de change EUR → USD dans une variable. |
| 2 | **La saisie** | Demander le montant en euros à l'utilisateur avec `input()`. |
| 3 | **Le résultat** | Calculer la conversion et l'afficher avec une f-string (2 décimales). |

## Solution

Le script [`convertisseur_eur_usd.py`](convertisseur_eur_usd.py) répond aux trois étapes.
Le cœur de l'exercice tient en quelques lignes :

```python
# 1. Le taux : récupéré en temps réel (voir le bonus ci-dessous)
taux_eur_usd, date_taux, source = recuperer_taux_eur_usd()

# 2. La saisie : montant en euros (la virgule française est acceptée)
saisie = input("Montant en euros (€) : ")
montant_eur = float(saisie.replace(",", "."))

# 3. Le résultat : conversion + affichage f-string à 2 décimales
montant_usd = montant_eur * taux_eur_usd
print(f"{montant_eur:.2f} € = {montant_usd:.2f} $")
```

### Bonus — taux de change en temps réel

Plutôt que de coder le taux en dur, on le récupère **en direct** auprès d'une API
publique gratuite et sans clé : [**Frankfurter**](https://www.frankfurter.app/)
(taux de référence de la **BCE**), avec [exchangerate-api](https://www.exchangerate-api.com/)
en secours. On utilise uniquement la **bibliothèque standard** (`urllib` + `json`) :
aucun package à installer.

```python
import json
import urllib.request

def recuperer_taux_eur_usd():
    url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
    requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(requete, timeout=8) as reponse:
        donnees = json.load(reponse)
    return float(donnees["rates"]["USD"])
```

> **Mode hors ligne** : si aucune API ne répond (pas de connexion), le script
> retombe automatiquement sur un taux de secours (`TAUX_PAR_DEFAUT = 1.08`)
> afin de fonctionner quand même.

### Notions abordées

- **Variable** : stockage du taux de change (`taux_eur_usd`).
- **`input()`** : lecture d'une valeur saisie au clavier (renvoie toujours une *chaîne*).
- **`float()`** : conversion de la chaîne en nombre décimal pour pouvoir calculer.
- **f-string** : `f"{valeur:.2f}"` formate le nombre avec exactement 2 décimales.
- **Appel d'API / JSON** (bonus) : `urllib.request` pour interroger un service web,
  `json` pour lire la réponse, et `try / except` pour gérer l'absence de réseau.

### Petit plus

`input()` renvoie une chaîne de caractères : il faut donc la convertir en nombre avec
`float()` avant de calculer. On remplace au passage la virgule par un point
(`"12,50"` → `12.50`) pour accepter la notation française.

## Exécution

```bash
python convertisseur_eur_usd.py
```

### Exemple

```
Taux EUR->USD : 1.1646  (source : Frankfurter / BCE, 2026-06-01)
Montant en euros (€) : 100
100.00 € = 116.46 $
```

```
Taux EUR->USD : 1.1646  (source : Frankfurter / BCE, 2026-06-01)
Montant en euros (€) : 250,75
250.75 € = 292.02 $
```

> Les montants en dollars varient d'un jour à l'autre puisque le taux est réel et actualisé.

## Rendu

- **Format** : un fichier `.py` ou `.ipynb`.
- **Échéance** : par mail **avant la séance 2 (12 h CET)**.
- **Destinataire** : voir le [README principal](../README.md) du dépôt.
