import pandas as pd
import numpy as np
from scipy import stats

def prepare_dataframe(users):
    """Convertit les utilisateurs en DataFrame Pandas"""
    rows = []
    for user in users:
        for log in user.daily_logs:
            rows.append({
                "name": user.name,
                "goal": user.goal,
                "date": log["date"],
                "steps": log["steps"],
                "calories": log["calories"],
                "workout": log["workout"]
            })
    return pd.DataFrame(rows)


def anova_calories_by_workout(df):
    """ANOVA : Est-ce que les calories brûlées diffèrent selon le type de workout ?"""
    print("\n📊 ANOVA - Calories par type de workout :")
    print("=" * 50)

    groups = [group["calories"].values for _, group in df.groupby("workout")]
    f_stat, p_value = stats.f_oneway(*groups)

    print(f"F-statistique : {f_stat:.4f}")
    print(f"P-valeur      : {p_value:.4f}")

    if p_value < 0.05:
        print("✅ Différence significative entre les workouts !")
    else:
        print("❌ Pas de différence significative entre les workouts.")


def linear_regression_steps(df):
    """Régression linéaire : Prédire les pas futurs"""
    print("\n📈 Régression linéaire - Prédiction des pas :")
    print("=" * 50)

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["day_number"] = (df["date"] - df["date"].min()).dt.days

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df["day_number"], df["steps"]
    )

    print(f"Pente         : {slope:.2f} pas/jour")
    print(f"R²            : {r_value**2:.4f}")
    print(f"P-valeur      : {p_value:.4f}")

    # Prédire les 7 prochains jours
    last_day = df["day_number"].max()
    print("\n🔮 Prédictions pour les 7 prochains jours :")
    for i in range(1, 8):
        predicted = intercept + slope * (last_day + i)
        print(f"  Jour +{i} : {predicted:.0f} pas")


def ttest_before_after(df):
    """T-test apparié : Impact de la Strength Training sur les calories"""
    print("\n🔬 T-test - Strength Training vs HIIT :")
    print("=" * 50)

    strength = df[df["workout"] == "Strength Training"]["calories"].values
    hiit = df[df["workout"] == "HIIT"]["calories"].values

    # Égaliser les tailles
    min_size = min(len(strength), len(hiit))
    strength = strength[:min_size]
    hiit = hiit[:min_size]

    t_stat, p_value = stats.ttest_rel(strength, hiit)

    print(f"Moyenne Strength Training : {np.mean(strength):.2f} cal")
    print(f"Moyenne HIIT              : {np.mean(hiit):.2f} cal")
    print(f"T-statistique             : {t_stat:.4f}")
    print(f"P-valeur                  : {p_value:.4f}")

    if p_value < 0.05:
        print("✅ Différence significative entre Strength Training et HIIT !")
    else:
        print("❌ Pas de différence significative.")