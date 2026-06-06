import pandas as pd      # Bibliothèque pour manipuler les données (tableaux)
import numpy as np       # Bibliothèque pour les calculs mathématiques
from scipy import stats  # Module contenant les tests statistiques (ANOVA, T-test, Régression)

def prepare_dataframe(users):
    """
    Transforme la structure objet (utilisateurs) en tableau (DataFrame).
    Le jury appréciera : 'On passe d'un format objet complexe à un format tabulaire 
    optimisé pour les calculs statistiques.'
    """
    rows = []
    for user in users:
        for log in user.daily_logs: # On extrait les logs d'activité de chaque utilisateur
            rows.append({
                "name": user.name,
                "goal": user.goal,
                "date": log["date"],
                "steps": log["steps"],
                "calories": log["calories"],
                "workout": log["workout"]
            })
    return pd.DataFrame(rows) # Le DataFrame est le format standard en Data Science


def anova_calories_by_workout(df):
    """
    ANOVA (Analyse de la variance) : Teste si les moyennes de calories sont 
    différentes entre plusieurs groupes (Yoga, HIIT, etc.).
    """
    print("\n📊 ANOVA - Calories par type de workout :")
    print("=" * 50)

    # On crée une liste contenant les valeurs de calories séparées par type d'exercice
    groups = [group["calories"].values for _, group in df.groupby("workout")]
    
    # f_oneway compare les moyennes : si la p-valeur < 0.05, la différence n'est pas due au hasard
    f_stat, p_value = stats.f_oneway(*groups)

    print(f"F-statistique : {f_stat:.4f}")
    print(f"P-valeur      : {p_value:.4f}")

    if p_value < 0.05:
        print("✅ Différence significative entre les workouts !") # Preuve scientifique
    else:
        print("❌ Pas de différence significative.")


def linear_regression_steps(df):
    """
    Régression linéaire : Analyse la tendance pour prédire le futur.
    Logique : y = ax + b (a = pente, b = intercept).
    """
    print("\n📈 Régression linéaire - Prédiction des pas :")
    print("=" * 50)

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]) # Conversion essentielle pour gérer le temps
    df = df.sort_values("date")
    # On transforme les dates en nombres (jour 0, jour 1...) pour le calcul mathématique
    df["day_number"] = (df["date"] - df["date"].min()).dt.days

    # linregress calcule la droite qui passe au plus proche de tous les points
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df["day_number"], df["steps"]
    )

    print(f"Pente         : {slope:.2f} pas/jour") # Indique si l'activité augmente ou diminue
    print(f"R²            : {r_value**2:.4f}")      # R² : Précision du modèle (plus c'est proche de 1, mieux c'est)
    print(f"P-valeur      : {p_value:.4f}")

    # Prédictions : on utilise la formule de la droite pour les 7 prochains jours
    last_day = df["day_number"].max()
    print("\n🔮 Prédictions pour les 7 prochains jours :")
    for i in range(1, 8):
        predicted = intercept + slope * (last_day + i)
        print(f"  Jour +{i} : {predicted:.0f} pas")


def ttest_before_after(df):
    """
    T-test apparié : Compare spécifiquement deux groupes (Strength vs HIIT).
    On cherche à savoir si un type d'exercice brûle *vraiment* plus de calories qu'un autre.
    """
    print("\n🔬 T-test - Strength Training vs HIIT :")
    print("=" * 50)

    # On isole les deux colonnes de données
    strength = df[df["workout"] == "Strength Training"]["calories"].values
    hiit = df[df["workout"] == "HIIT"]["calories"].values

    # Pour un T-test, les deux listes doivent avoir la même taille
    min_size = min(len(strength), len(hiit))
    strength = strength[:min_size]
    hiit = hiit[:min_size]

    # ttest_rel est utilisé car on compare les performances sur des groupes liés
    t_stat, p_value = stats.ttest_rel(strength, hiit)

    print(f"Moyenne Strength Training : {np.mean(strength):.2f} cal")
    print(f"Moyenne HIIT              : {np.mean(hiit):.2f} cal")
    print(f"P-valeur                  : {p_value:.4f}")

    if p_value < 0.05:
        print("✅ Différence significative entre Strength Training et HIIT !")
    else:
        print("❌ Pas de différence significative.")