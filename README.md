# UE 4 — Management & Data Science · Exercices Python

Ce dépôt regroupe les exercices Python réalisés dans le cadre de l'**UE 4 · Management & Data Science** (MBA).

Chaque séance possède son propre dossier (`seance-01`, `seance-02`, …) contenant le ou les scripts ainsi qu'une courte documentation expliquant l'énoncé, la solution et comment l'exécuter.

## Structure du dépôt

```
ue4-exercises/
├── README.md            ← ce fichier
├── .gitignore
├── seance-01/
│   ├── README.md        ← doc de l'exercice de la séance
│   └── convertisseur_eur_usd.py
└── seance-02/
    ├── README.md
    ├── pair_ou_impair.py
    ├── table_de_multiplication.py
    └── somme_jusqu_a_n.py
```

## Prérequis

- [Python 3.14.5](https://www.python.org/downloads/) (version utilisée pour ce dépôt).
- Aucun package externe : uniquement la bibliothèque standard.
- Une connexion internet est utile pour la séance 01 (taux de change en temps réel), mais un repli hors ligne est prévu.

## Lancer un exercice

```bash
python seance-01/convertisseur_eur_usd.py
```

## Workflow Git

- `main` — version stable / rendue.
- `development` — branche de travail où sont développés les exercices.

## Séances

| Séance | Thème | Exercice |
|:------:|-------|----------|
| 01 | Synthèse — variables, `input()`, f-strings | [Convertisseur € → $](seance-01/README.md) |
| 02 | Conditions & boucles (`if`, `for`, `range`, `%`) | [Exercices guidés](seance-02/README.md) |

## Rendu des exercices

- **Format** : un fichier `.py` ou `.ipynb` par exercice.
- **Échéance** : par mail avant la séance suivante (voir la consigne de chaque séance).
- **Professeur / destinataire** : **romain@willmann.biz**

---

*Auteur : Nicolas Duchemann — MBA, UE 4 Management & Data Science.*
