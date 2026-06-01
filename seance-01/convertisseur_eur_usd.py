"""
Séance 1 — Exercice de synthèse : convertisseur € → $

Étapes demandées :
    1. Le taux    : définir un taux de change EUR → USD dans une variable.
    2. La saisie  : demander le montant en euros à l'utilisateur avec input().
    3. Le résultat: calculer la conversion et l'afficher avec une f-string (2 décimales).

Bonus : le taux n'est pas codé en dur, il est récupéré EN TEMPS RÉEL via une API
publique gratuite (Frankfurter, basée sur les taux de référence de la BCE).
En l'absence de connexion, on retombe automatiquement sur un taux de secours.

Uniquement la bibliothèque standard (urllib + json) : aucun package à installer.

UE 4 · Management & Data Science
"""

import json
import urllib.error
import urllib.request

# Taux utilisé en dernier recours si aucune API n'est joignable (mode hors ligne).
TAUX_PAR_DEFAUT = 1.08


def recuperer_taux_eur_usd():
    """Récupère le taux EUR -> USD en temps réel.

    Renvoie un tuple (taux, date, source). Essaie chaque API dans l'ordre ;
    si toutes échouent (pas de connexion, API en panne...), renvoie le taux
    de secours pour que le programme fonctionne quand même.
    """
    apis = [
        ("https://api.frankfurter.app/latest?from=EUR&to=USD", "Frankfurter / BCE"),
        ("https://open.er-api.com/v6/latest/EUR", "exchangerate-api"),
    ]
    for url, source in apis:
        try:
            requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(requete, timeout=8) as reponse:
                donnees = json.load(reponse)
            taux = float(donnees["rates"]["USD"])
            date = donnees.get("date", "aujourd'hui")
            return taux, date, source
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError):
            continue  # cette API a échoué : on tente la suivante
    return TAUX_PAR_DEFAUT, "taux de secours", "hors ligne"


# 1. Le taux : récupéré en temps réel (variable taux_eur_usd), avec repli automatique.
taux_eur_usd, date_taux, source = recuperer_taux_eur_usd()
print(f"Taux EUR->USD : {taux_eur_usd:.4f}  (source : {source}, {date_taux})")

# 2. La saisie : montant en euros. La virgule française (ex : "12,50") est acceptée.
saisie = input("Montant en euros (€) : ")
montant_eur = float(saisie.replace(",", "."))

# 3. Le résultat : conversion puis affichage avec une f-string à 2 décimales.
montant_usd = montant_eur * taux_eur_usd
print(f"{montant_eur:.2f} € = {montant_usd:.2f} $")
