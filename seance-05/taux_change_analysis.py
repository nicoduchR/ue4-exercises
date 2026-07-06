"""
Séance 5 — Contrôle continu : analyse du taux EUR/USD

Le projet noté qui mobilise tout le cours :
    1. Télécharger : taux EUR/USD des 2 dernières années → eur_usd.csv.
    2. Préparer    : charger dans Pandas, index temporel trié, traiter les
                     jours manquants.
    3. Explorer    : rendement journalier en %, statistiques descriptives.
    4. Prévoir     : régression linéaire pour prédire le lendemain, calculer
                     le RMSE.

Livrables : taux_change_analysis.py + graphiques + commentaire — par mail.

Dépendances : pandas, matplotlib, scikit-learn
    pip install pandas matplotlib scikit-learn

UE 4 · Management & Data Science
"""

import json
import math
import os
import urllib.error
import urllib.request
from datetime import date, timedelta

import matplotlib

matplotlib.use("Agg")  # rendu en fichiers PNG, sans ouvrir de fenêtre
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

# Tous les fichiers produits sont écrits à côté de ce script, quel que soit
# le dossier depuis lequel on lance le programme.
DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_CSV = os.path.join(DOSSIER, "eur_usd.csv")
FICHIER_COMMENTAIRE = os.path.join(DOSSIER, "commentaire.txt")
DOSSIER_GRAPHIQUES = os.path.join(DOSSIER, "graphiques")

# Taux de référence utilisé pour générer des données de secours hors ligne.
TAUX_DE_SECOURS = 1.08

# Part de l'historique réservée à l'évaluation du modèle (20 % les plus récents).
PART_TEST = 0.2


# ---------------------------------------------------------------------------
# Étape 1 — Télécharger
# ---------------------------------------------------------------------------

def telecharger_historique(annees=2):
    """Télécharge le taux EUR -> USD des `annees` dernières années.

    Renvoie un tuple (historique, source) où `historique` est une liste de
    tuples (date_iso, taux) triée par date croissante. L'API Frankfurter
    (taux de référence de la BCE) ne cote pas les week-ends ni les jours
    fériés : ces trous seront traités à l'étape 2. En cas d'échec réseau,
    on retombe sur un jeu de données de secours déterministe pour que le
    programme reste démontrable hors ligne.
    """
    fin = date.today()
    debut = fin - timedelta(days=annees * 365)
    url = (
        f"https://api.frankfurter.app/{debut.isoformat()}..{fin.isoformat()}"
        "?from=EUR&to=USD"
    )
    try:
        requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(requete, timeout=15) as reponse:
            donnees = json.load(reponse)
        rates = donnees["rates"]  # {"2024-07-08": {"USD": 1.08}, ...}
        historique = sorted(
            (jour, float(valeurs["USD"])) for jour, valeurs in rates.items()
        )
        if not historique:
            raise ValueError("réponse vide")
        return historique, "Frankfurter / BCE"
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError):
        return _historique_de_secours(debut, fin), "hors ligne (données de secours)"


def _historique_de_secours(debut, fin):
    """Génère 2 ans de données plausibles (jours ouvrés) autour du taux de secours.

    Sert uniquement quand l'API est injoignable. L'oscillation combine une
    tendance lente et un cycle court, de façon déterministe (pas d'aléatoire)
    pour rester reproductible.
    """
    historique = []
    jour = debut
    i = 0
    while jour <= fin:
        if jour.weekday() < 5:  # 0 = lundi ... 4 = vendredi : on ignore le week-end
            taux = TAUX_DE_SECOURS + 0.04 * math.sin(i / 60) + 0.01 * math.sin(i / 7)
            historique.append((jour.isoformat(), round(taux, 4)))
            i += 1
        jour += timedelta(days=1)
    return historique


def ecrire_csv(chemin, historique):
    """Écrit l'historique téléchargé dans eur_usd.csv (date, taux_eur_usd)."""
    df = pd.DataFrame(historique, columns=["date", "taux_eur_usd"])
    df.to_csv(chemin, index=False)


# ---------------------------------------------------------------------------
# Étape 2 — Préparer
# ---------------------------------------------------------------------------

def preparer(chemin):
    """Charge le CSV dans Pandas et traite les jours manquants.

    - index temporel (`DatetimeIndex`) trié par date croissante ;
    - réindexation sur TOUS les jours calendaires (`asfreq("D")`) : les
      week-ends et jours fériés apparaissent alors comme NaN ;
    - remplissage par propagation du dernier taux connu (`ffill`) : le
      week-end, le taux applicable reste celui du dernier fixing BCE.

    Renvoie (df, nb_jours_combles).
    """
    df = pd.read_csv(chemin, parse_dates=["date"], index_col="date")
    df = df.sort_index()
    df = df.asfreq("D")
    nb_combles = int(df["taux_eur_usd"].isna().sum())
    df["taux_eur_usd"] = df["taux_eur_usd"].ffill()
    return df, nb_combles


# ---------------------------------------------------------------------------
# Étape 3 — Explorer
# ---------------------------------------------------------------------------

def explorer(df):
    """Calcule le rendement journalier en % et ses statistiques descriptives.

    Le rendement du jour t est la variation relative par rapport à la veille :
    (taux_t - taux_{t-1}) / taux_{t-1} * 100.
    """
    df["rendement_pct"] = df["taux_eur_usd"].pct_change() * 100
    return df["rendement_pct"].describe()


def tracer_graphiques(df, y_test, predictions, dates_test):
    """Produit les trois graphiques du rendu dans le dossier graphiques/."""
    os.makedirs(DOSSIER_GRAPHIQUES, exist_ok=True)

    # 1. Évolution du taux sur 2 ans + moyenne mobile 30 jours.
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["taux_eur_usd"], linewidth=0.9, label="Taux EUR/USD")
    ax.plot(
        df.index,
        df["taux_eur_usd"].rolling(30).mean(),
        linewidth=1.6,
        label="Moyenne mobile 30 j",
    )
    ax.set_title("Taux EUR/USD — 2 dernières années")
    ax.set_ylabel("1 EUR en USD")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(DOSSIER_GRAPHIQUES, "01_taux_eur_usd.png"), dpi=150)
    plt.close(fig)

    # 2. Rendements journaliers : série temporelle + histogramme.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    ax1.plot(df.index, df["rendement_pct"], linewidth=0.7)
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_title("Rendement journalier (%)")
    ax1.set_ylabel("%")
    ax1.grid(alpha=0.3)
    ax2.hist(df["rendement_pct"].dropna(), bins=60)
    ax2.set_title("Distribution des rendements")
    ax2.set_xlabel("%")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(
        os.path.join(DOSSIER_GRAPHIQUES, "02_rendements_journaliers.png"), dpi=150
    )
    plt.close(fig)

    # 3. Prévision : taux réel vs taux prédit sur la période de test.
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates_test, y_test, linewidth=1.2, label="Taux réel")
    ax.plot(
        dates_test,
        predictions,
        linewidth=1.2,
        linestyle="--",
        label="Taux prédit (régression)",
    )
    ax.set_title("Prévision du lendemain — période de test (20 % la plus récente)")
    ax.set_ylabel("1 EUR en USD")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(
        os.path.join(DOSSIER_GRAPHIQUES, "03_prevision_regression.png"), dpi=150
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Étape 4 — Prévoir
# ---------------------------------------------------------------------------

def prevoir(df):
    """Régression linéaire : prédire le taux du lendemain à partir de celui du jour.

    On construit un couple (X, y) où X est le taux du jour t et y le taux du
    jour t+1, puis on découpe SANS mélanger (données temporelles) : les 80 %
    les plus anciens entraînent le modèle, les 20 % les plus récents servent
    à mesurer l'erreur (RMSE). Le RMSE d'un modèle naïf "demain = aujourd'hui"
    sert de point de comparaison.
    """
    couples = pd.DataFrame(
        {
            "taux_du_jour": df["taux_eur_usd"],
            "taux_du_lendemain": df["taux_eur_usd"].shift(-1),
        }
    ).dropna()

    X = couples[["taux_du_jour"]].to_numpy()
    y = couples["taux_du_lendemain"].to_numpy()

    n_test = int(len(couples) * PART_TEST)
    X_train, X_test = X[:-n_test], X[-n_test:]
    y_train, y_test = y[:-n_test], y[-n_test:]

    modele = LinearRegression()
    modele.fit(X_train, y_train)
    predictions = modele.predict(X_test)

    rmse = root_mean_squared_error(y_test, predictions)
    rmse_naif = root_mean_squared_error(y_test, X_test.ravel())

    dernier_taux = float(df["taux_eur_usd"].iloc[-1])
    prevision_demain = float(modele.predict([[dernier_taux]])[0])

    return {
        "pente": float(modele.coef_[0]),
        "intercept": float(modele.intercept_),
        "rmse": rmse,
        "rmse_naif": rmse_naif,
        "n_train": len(X_train),
        "n_test": n_test,
        "dernier_taux": dernier_taux,
        "prevision_demain": prevision_demain,
        "y_test": y_test,
        "predictions": predictions,
        "dates_test": couples.index[-n_test:],
    }


# ---------------------------------------------------------------------------
# Commentaire (livrable)
# ---------------------------------------------------------------------------

def construire_commentaire(df, source, nb_combles, stats_rendement, resultat):
    """Rédige le commentaire du rendu : chiffres clés + interprétation."""
    ecart = resultat["rmse"] - resultat["rmse_naif"]
    if ecart < 0:
        comparaison = "fait legerement mieux que"
    elif ecart == 0:
        comparaison = "fait exactement aussi bien que"
    else:
        comparaison = "ne fait pas mieux que"

    lignes = [
        "Commentaire - controle continu : analyse du taux EUR/USD",
        "=" * 60,
        f"Source des donnees : {source}",
        f"Periode analysee   : du {df.index[0].date()} au {df.index[-1].date()}"
        f" ({len(df)} jours calendaires)",
        f"Jours combles      : {nb_combles} (week-ends et feries, remplis par"
        " propagation du dernier taux connu)",
        "",
        "1. Exploration",
        f"   Rendement journalier moyen : {stats_rendement['mean']:+.4f} %",
        f"   Volatilite (ecart-type)    : {stats_rendement['std']:.4f} %",
        f"   Pire jour                  : {stats_rendement['min']:+.4f} %",
        f"   Meilleur jour              : {stats_rendement['max']:+.4f} %",
        "   Le rendement moyen est proche de zero et la distribution est",
        "   centree : sur 2 ans, le taux evolue par petites variations",
        "   quotidiennes, sans derive journaliere marquee. Le pic de",
        "   rendements a exactement 0 % sur l'histogramme correspond aux",
        "   week-ends et jours feries combles par ffill : le taux n'y bouge",
        "   pas, par construction.",
        "",
        "2. Prevision (regression lineaire)",
        f"   Modele : taux_demain = {resultat['pente']:.4f} x taux_du_jour"
        f" {resultat['intercept']:+.4f}",
        f"   Entrainement / test : {resultat['n_train']} / {resultat['n_test']}"
        " jours (decoupage chronologique 80/20)",
        f"   RMSE (regression)   : {resultat['rmse']:.5f} USD",
        f"   RMSE (naif, demain = aujourd'hui) : {resultat['rmse_naif']:.5f} USD",
        f"   Dernier taux connu  : {resultat['dernier_taux']:.4f} USD",
        f"   Prevision pour demain : {resultat['prevision_demain']:.4f} USD",
        "",
        "3. Interpretation",
        f"   La pente est proche de 1 et l'ordonnee a l'origine proche de 0 :",
        "   la meilleure prediction lineaire du taux de demain est presque",
        f"   le taux d'aujourd'hui. La regression {comparaison} le modele",
        "   naif \"demain = aujourd'hui\", ce qui est typique d'un taux de",
        "   change : il se comporte quasiment comme une marche aleatoire, et",
        "   l'information d'hier est deja contenue dans le prix du jour.",
        "   L'interet du modele n'est donc pas de \"battre le marche\" mais",
        f"   de quantifier l'incertitude : l'erreur type est d'environ",
        f"   {resultat['rmse']:.4f} USD, soit l'ordre de grandeur du mouvement",
        "   qu'on peut attendre d'un jour a l'autre.",
    ]
    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------

def main():
    # 1. Télécharger : 2 ans d'historique via l'API (repli hors ligne automatique).
    print("1. Telechargement du taux EUR/USD (2 dernieres annees)...")
    historique, source = telecharger_historique(annees=2)
    ecrire_csv(FICHIER_CSV, historique)
    print(f"   -> {len(historique)} releves (source : {source})")
    print(f"   -> CSV ecrit : {FICHIER_CSV}")

    # 2. Préparer : Pandas, index temporel trié, jours manquants comblés.
    print("2. Preparation (index temporel, jours manquants)...")
    df, nb_combles = preparer(FICHIER_CSV)
    print(f"   -> {len(df)} jours calendaires, {nb_combles} jours combles (ffill)")

    # 3. Explorer : rendement journalier en % et statistiques descriptives.
    print("3. Exploration : rendements journaliers (%)...")
    stats_rendement = explorer(df)
    print(stats_rendement.to_string())

    # 4. Prévoir : régression linéaire + RMSE.
    print("4. Prevision par regression lineaire...")
    resultat = prevoir(df)
    print(f"   -> RMSE regression : {resultat['rmse']:.5f} USD")
    print(f"   -> RMSE naif       : {resultat['rmse_naif']:.5f} USD")
    print(f"   -> Prevision demain : {resultat['prevision_demain']:.4f} USD")

    # Livrables : graphiques + commentaire.
    tracer_graphiques(
        df, resultat["y_test"], resultat["predictions"], resultat["dates_test"]
    )
    print(f"Graphiques ecrits : {DOSSIER_GRAPHIQUES}")

    commentaire = construire_commentaire(
        df, source, nb_combles, stats_rendement, resultat
    )
    with open(FICHIER_COMMENTAIRE, "w", encoding="utf-8") as fichier:
        fichier.write(commentaire + "\n")
    print(f"Commentaire ecrit : {FICHIER_COMMENTAIRE}\n")

    print(commentaire)


if __name__ == "__main__":
    main()
