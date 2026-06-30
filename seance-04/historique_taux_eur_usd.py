"""
Séance 4 — Exercice de synthèse : historique du taux EUR → USD

Étapes demandées :
    1. Récupérer  : le taux EUR/USD des 30 derniers jours via une API.
    2. Stocker & analyser : écrire un CSV, le relire, calculer moyenne, min, max.
    3. Robustesse : afficher les dates du min/max et gérer l'absence de réseau.

À rendre : un programme qui produit le CSV + un mini-rapport texte.

Uniquement la bibliothèque standard (urllib, json, csv, datetime, statistics) :
aucun package à installer.

UE 4 · Management & Data Science
"""

import csv
import json
import math
import os
import statistics
import urllib.error
import urllib.request
from datetime import date, timedelta

# Le CSV et le rapport sont écrits à côté de ce script, quel que soit le dossier
# depuis lequel on lance le programme.
DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_CSV = os.path.join(DOSSIER, "taux_eur_usd_30j.csv")
FICHIER_RAPPORT = os.path.join(DOSSIER, "rapport.txt")

# Taux de référence utilisé pour générer des données de secours hors ligne.
TAUX_DE_SECOURS = 1.08


def recuperer_historique(jours=30):
    """Récupère le taux EUR -> USD des `jours` derniers jours.

    Renvoie un tuple (historique, source) où `historique` est une liste de
    tuples (date_iso, taux) triée par date croissante. L'API Frankfurter
    (taux de référence de la BCE) ne cote pas les week-ends : on obtient donc
    les jours ouvrés de la période. En cas d'échec réseau, on retombe sur un
    jeu de données de secours pour que le programme fonctionne quand même.
    """
    fin = date.today()
    debut = fin - timedelta(days=jours)
    url = (
        f"https://api.frankfurter.app/{debut.isoformat()}..{fin.isoformat()}"
        "?from=EUR&to=USD"
    )
    try:
        requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(requete, timeout=10) as reponse:
            donnees = json.load(reponse)
        rates = donnees["rates"]  # {"2026-06-01": {"USD": 1.08}, ...}
        historique = sorted(
            (jour, float(valeurs["USD"])) for jour, valeurs in rates.items()
        )
        if not historique:
            raise ValueError("réponse vide")
        return historique, "Frankfurter / BCE"
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError):
        return _historique_de_secours(debut, fin), "hors ligne (données de secours)"


def _historique_de_secours(debut, fin):
    """Génère un historique plausible (jours ouvrés) autour du taux de secours.

    Sert uniquement quand l'API est injoignable, afin que l'analyse et le CSV
    restent démontrables même sans connexion internet. L'oscillation est
    déterministe (pas d'aléatoire) pour rester reproductible.
    """
    historique = []
    jour = debut
    i = 0
    while jour <= fin:
        if jour.weekday() < 5:  # 0 = lundi ... 4 = vendredi : on ignore le week-end
            taux = TAUX_DE_SECOURS + 0.02 * math.sin(i / 3)
            historique.append((jour.isoformat(), round(taux, 4)))
            i += 1
        jour += timedelta(days=1)
    return historique


def ecrire_csv(chemin, historique):
    """Écrit l'historique dans un fichier CSV (colonnes : date, taux_eur_usd)."""
    with open(chemin, "w", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        writer.writerow(["date", "taux_eur_usd"])
        writer.writerows(historique)


def lire_csv(chemin):
    """Relit le CSV et renvoie une liste de tuples (date_iso, taux)."""
    historique = []
    with open(chemin, "r", newline="", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            historique.append((ligne["date"], float(ligne["taux_eur_usd"])))
    return historique


def analyser(historique):
    """Calcule moyenne, minimum et maximum (avec leurs dates) de l'historique."""
    taux = [valeur for _, valeur in historique]
    date_min, taux_min = min(historique, key=lambda couple: couple[1])
    date_max, taux_max = max(historique, key=lambda couple: couple[1])
    return {
        "nombre": len(historique),
        "moyenne": statistics.mean(taux),
        "min": taux_min,
        "date_min": date_min,
        "max": taux_max,
        "date_max": date_max,
        "debut": historique[0][0],
        "fin": historique[-1][0],
    }


def construire_rapport(stats, source):
    """Met en forme un mini-rapport texte lisible à partir des statistiques."""
    lignes = [
        "Rapport — historique du taux EUR -> USD (30 derniers jours)",
        "=" * 58,
        f"Source des donnees : {source}",
        f"Periode analysee   : du {stats['debut']} au {stats['fin']}",
        f"Nombre de releves  : {stats['nombre']} (jours ouvres)",
        "",
        f"Taux moyen   : {stats['moyenne']:.4f} USD",
        f"Taux minimum : {stats['min']:.4f} USD  (le {stats['date_min']})",
        f"Taux maximum : {stats['max']:.4f} USD  (le {stats['date_max']})",
        f"Amplitude    : {stats['max'] - stats['min']:.4f} USD",
    ]
    return "\n".join(lignes)


def main():
    # 1. Récupérer : 30 derniers jours via l'API (repli hors ligne automatique).
    print("Recuperation de l'historique EUR -> USD (30 derniers jours)...")
    historique, source = recuperer_historique(30)
    print(f"  -> {len(historique)} releves  (source : {source})")

    # 2. Stocker : on écrit le CSV puis on le RELIT (preuve qu'il est exploitable).
    ecrire_csv(FICHIER_CSV, historique)
    print(f"CSV ecrit     : {FICHIER_CSV}")
    historique = lire_csv(FICHIER_CSV)

    # 3. Analyser + robustesse : stats, dates du min/max, et mini-rapport texte.
    stats = analyser(historique)
    rapport = construire_rapport(stats, source)
    with open(FICHIER_RAPPORT, "w", encoding="utf-8") as fichier:
        fichier.write(rapport + "\n")
    print(f"Rapport ecrit : {FICHIER_RAPPORT}\n")

    print(rapport)


if __name__ == "__main__":
    main()
