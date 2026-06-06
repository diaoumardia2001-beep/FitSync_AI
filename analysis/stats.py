import pandas as pd
import numpy as np
from scipy import stats


def prepare_dataframe(users):
    """
    Convertit une liste d'utilisateurs (dicts)
    en DataFrame Pandas pour l'analyse
    """
    rows = []
    for user in users:
        name = user.get("name", "Unknown")
        goal = user.get("goal", "unknown")
        for log in user.get("daily_logs", []):
            rows.append({
                "name": name,
                "goal": goal,
                "date": log.get("date", ""),
                "steps": log.get("steps", 0),
                "calories": log.get("calories", 0),
                "workout": log.get("workout", "Unknown")
            })
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df


def anova_calories_by_workout(df):
    """
    ANOVA — scipy.stats.f_oneway
    Question : Les calories brûlées diffèrent-elles
    significativement selon le type de workout ?
    """
    print(f"\n{'='*50}")
    print("📊 ANOVA — Calories par type de workout")
    print(f"{'='*50}")

    # Grouper par workout
    groups = [
        group["calories"].values
        for _, group in df.groupby("workout")
        if len(group) > 1
    ]

    if len(groups) < 2:
        print("⚠️ Pas assez de groupes pour ANOVA")
        return None

    f_stat, p_value = stats.f_oneway(*groups)

    # Statistiques par workout
    summary = df.groupby("workout")["calories"].agg([
        "mean", "std", "count"
    ]).round(2)
    print(summary)

    print(f"\nF-statistique : {f_stat:.4f}")
    print(f"P-valeur      : {p_value:.4f}")

    if p_value < 0.05:
        print(
            "✅ Différence SIGNIFICATIVE entre "
            "les workouts (p < 0.05)"
        )
    else:
        print(
            "❌ Pas de différence significative "
            "entre les workouts (p > 0.05)"
        )

    return {
        "f_stat": round(float(f_stat), 4),
        "p_value": round(float(p_value), 4),
        "significant": bool(p_value < 0.05),
        "summary": summary.to_dict()
    }


def linear_regression_steps(df):
    """
    Régression linéaire — scipy.stats.linregress
    Prédit le nombre de pas futurs
    basé sur les données historiques
    """
    print(f"\n{'='*50}")
    print("📈 RÉGRESSION LINÉAIRE — Prédiction des pas")
    print(f"{'='*50}")

    df = df.copy().sort_values("date")
    df["day_number"] = (
        df["date"] - df["date"].min()
    ).dt.days

    # Grouper par jour (moyenne)
    daily = df.groupby("day_number")[
        "steps"
    ].mean().reset_index()

    slope, intercept, r_value, p_value, std_err = (
        stats.linregress(
            daily["day_number"],
            daily["steps"]
        )
    )

    print(f"Pente         : {slope:.2f} pas/jour")
    print(f"Intercept     : {intercept:.2f}")
    print(f"R²            : {r_value**2:.4f}")
    print(f"P-valeur      : {p_value:.4f}")
    print(f"Erreur std    : {std_err:.2f}")

    # Prédictions J+1 à J+7
    last_day = daily["day_number"].max()
    predictions = []
    print(f"\n🔮 Prédictions (7 prochains jours) :")
    for i in range(1, 8):
        predicted = intercept + slope * (last_day + i)
        predicted = max(0, int(predicted))
        predictions.append({
            "day": f"J+{i}",
            "predicted_steps": predicted
        })
        print(f"  J+{i} : {predicted:,} pas")

    trend = "📈 En hausse" if slope > 0 else "📉 En baisse"
    print(f"\nTendance : {trend}")

    return {
        "slope": round(float(slope), 4),
        "intercept": round(float(intercept), 4),
        "r_squared": round(float(r_value**2), 4),
        "p_value": round(float(p_value), 4),
        "predictions": predictions,
        "trend": trend,
        "daily_data": daily.to_dict()
    }


def ttest_before_after(df):
    """
    T-test apparié — scipy.stats.ttest_rel
    Compare Strength Training vs HIIT
    Question : Y a-t-il une différence significative
    de calories entre ces deux workouts ?
    """
    print(f"\n{'='*50}")
    print("⚖️  T-TEST — Strength Training vs HIIT")
    print(f"{'='*50}")

    strength = df[
        df["workout"] == "Strength Training"
    ]["calories"].values

    hiit = df[
        df["workout"] == "HIIT"
    ]["calories"].values

    if len(strength) == 0 or len(hiit) == 0:
        print("⚠️ Données insuffisantes pour le T-test")
        return None

    # Égaliser les tailles
    min_size = min(len(strength), len(hiit))
    strength = strength[:min_size]
    hiit = hiit[:min_size]

    t_stat, p_value = stats.ttest_rel(strength, hiit)

    print(
        f"Moyenne Strength Training : "
        f"{np.mean(strength):.2f} cal"
    )
    print(f"Moyenne HIIT              : "
          f"{np.mean(hiit):.2f} cal")
    print(f"T-statistique             : {t_stat:.4f}")
    print(f"P-valeur                  : {p_value:.4f}")

    if p_value < 0.05:
        better = (
            "Strength Training"
            if np.mean(strength) > np.mean(hiit)
            else "HIIT"
        )
        print(
            f"✅ Différence SIGNIFICATIVE — "
            f"{better} brûle plus de calories"
        )
    else:
        print(
            "❌ Pas de différence significative "
            "entre Strength Training et HIIT"
        )

    return {
        "t_stat": round(float(t_stat), 4),
        "p_value": round(float(p_value), 4),
        "significant": bool(p_value < 0.05),
        "mean_strength": round(float(np.mean(strength)), 2),
        "mean_hiit": round(float(np.mean(hiit)), 2)
    }


def weekly_analysis(df):
    """
    Analyse hebdomadaire avec Pandas
    Calcule totaux et moyennes par semaine
    """
    print(f"\n{'='*50}")
    print("📅 ANALYSE HEBDOMADAIRE")
    print(f"{'='*50}")

    df = df.copy()
    df["week"] = df["date"].dt.isocalendar().week

    weekly = df.groupby("week").agg(
        total_steps=("steps", "sum"),
        total_calories=("calories", "sum"),
        avg_steps=("steps", "mean"),
        avg_calories=("calories", "mean"),
        sessions=("workout", "count")
    ).round(2)

    print(weekly)
    return weekly


def full_statistical_analysis(users):
    """
    Lance toutes les analyses statistiques
    """
    print("\n🔬 ANALYSE STATISTIQUE COMPLÈTE")
    print("━" * 50)

    df = prepare_dataframe(users)

    anova_result = anova_calories_by_workout(df)
    regression_result = linear_regression_steps(df)
    ttest_result = ttest_before_after(df)
    weekly_result = weekly_analysis(df)

    return {
        "anova": anova_result,
        "regression": regression_result,
        "ttest": ttest_result,
        "weekly": weekly_result,
        "dataframe": df
    }