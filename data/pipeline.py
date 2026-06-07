import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()

GOALS = ["weight_loss", "strength", "cardio", "flexibility"]
WORKOUTS = [
    "Yoga", "Running", "HIIT",
    "Strength Training", "Cycling", "Walking"
]


def collect_raw_data(n_users=50, n_days=30):
    rows = []
    for i in range(n_users):
        name = fake.name()
        age = random.randint(18, 65)
        goal = random.choice(GOALS)
        user_id = i + 1

        for day in range(n_days):
            date = fake.date_between(
                start_date="-30d",
                end_date="today"
            ).strftime("%Y-%m-%d")

            steps = (
                random.randint(1000, 20000)
                if random.random() > 0.15
                else None
            )

            cal_type = random.random()
            if cal_type < 0.70:
                calories = random.randint(150, 700)
            elif cal_type < 0.85:
                calories = random.randint(1500, 3000)
            elif cal_type < 0.92:
                calories = -random.randint(10, 100)
            else:
                calories = None

            workout = random.choice(
                WORKOUTS + [None, "", "  "]
            )

            hr_type = random.random()
            if hr_type < 0.75:
                heart_rate = random.randint(60, 180)
            elif hr_type < 0.90:
                heart_rate = random.randint(300, 500)
            else:
                heart_rate = None

            sleep_type = random.random()
            if sleep_type < 0.75:
                sleep_hours = round(random.uniform(4, 10), 1)
            elif sleep_type < 0.90:
                sleep_hours = round(random.uniform(20, 30), 1)
            else:
                sleep_hours = None

            weight_kg = (
                round(random.uniform(45, 120), 1)
                if random.random() > 0.20
                else None
            )

            row = {
                "user_id": user_id,
                "name": name,
                "age": age,
                "goal": goal,
                "date": date,
                "steps": steps,
                "calories": calories,
                "workout": workout,
                "heart_rate": heart_rate,
                "sleep_hours": sleep_hours,
                "weight_kg": weight_kg
            }
            rows.append(row)

            if random.random() < 0.05:
                rows.append(row.copy())

    df = pd.DataFrame(rows)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_data.csv", index=False)
    df.to_json(
        "data/raw_data.json",
        orient="records",
        indent=2
    )

    print(f"\n  📥  Collecte terminée")
    print(f"       Lignes        : {len(df)}")
    print(f"       Manquantes    : {df.isnull().sum().sum()}")
    print(f"       Doublons      : {df.duplicated().sum()}")

    return df


def clean_data(df):
    report = {}
    df_clean = df.copy()

    # 1. MISSING VALUES BEFORE
    missing_before = df_clean.isnull().sum().sum()
    report["missing_before"] = int(missing_before)

    # 2. WORKOUT CLEANING (avant tout groupby)
    df_clean["workout"] = df_clean["workout"].replace(
        ["", "  ", None], "Unknown"
    )
    df_clean["workout"] = df_clean["workout"].fillna("Unknown")
    df_clean["workout"] = df_clean["workout"].str.strip()
    df_clean.loc[
        df_clean["workout"] == "", "workout"
    ] = "Unknown"

    # 3. STEPS CLEANING
    df_clean["steps"] = df_clean.groupby("goal")["steps"].transform(
        lambda x: x.fillna(x.median())
    )
    df_clean["steps"] = df_clean["steps"].fillna(0)

    # 4. CALORIES CLEANING
    df_clean["calories"] = df_clean.groupby("workout")["calories"].transform(
        lambda x: x.fillna(x.median())
    )
    df_clean["calories"] = df_clean["calories"].fillna(
        df_clean["calories"].median()
    )
    # Securite : remplacer NaN restants
    df_clean["calories"] = df_clean["calories"].fillna(300)

    # 5. OTHER NUMERIC CLEANING
    df_clean["heart_rate"] = df_clean["heart_rate"].fillna(
        df_clean["heart_rate"].median()
    )
    df_clean["sleep_hours"] = df_clean["sleep_hours"].fillna(
        df_clean["sleep_hours"].median()
    )
    df_clean["weight_kg"] = df_clean["weight_kg"].fillna(
        df_clean["weight_kg"].median()
    )

    # 6. DUPLICATES
    dupl_before = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    report["duplicates_removed"] = int(
        dupl_before - df_clean.duplicated().sum()
    )
    print(f"  ✅ Doublons supprimés : {report['duplicates_removed']}")

    # 7. OUTLIERS (IQR METHOD)
    def remove_outliers_iqr(df, col, factor=1.5):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        mask = (df[col] < lower) | (df[col] > upper)
        df.loc[mask, col] = df[col].median()
        return df, int(mask.sum())

    total_outliers = 0
    for col in ["steps", "calories", "heart_rate", "sleep_hours"]:
        df_clean, n = remove_outliers_iqr(df_clean, col)
        report[f"outliers_{col}"] = n
        total_outliers += n
    print(f"  ✅ Outliers traités : {total_outliers}")

    # 8. IMPOSSIBLE VALUES FIX
    neg_cal = (df_clean["calories"] < 0).sum()
    df_clean.loc[df_clean["calories"] < 0, "calories"] = (
        df_clean["calories"].median()
    )
    df_clean.loc[df_clean["heart_rate"] > 220, "heart_rate"] = 100
    df_clean.loc[df_clean["heart_rate"] < 40, "heart_rate"] = 60
    df_clean.loc[df_clean["sleep_hours"] > 14, "sleep_hours"] = 7.0
    df_clean.loc[df_clean["steps"] < 0, "steps"] = 0
    report["impossible_values"] = int(neg_cal)
    print(f"  ✅ Valeurs impossibles corrigées : {neg_cal}")

    # 9. FINAL TYPE FIX
    df_clean["date"] = pd.to_datetime(df_clean["date"])
    df_clean["age"] = df_clean["age"].fillna(0).astype(int)
    df_clean["steps"] = df_clean["steps"].fillna(0).astype(int)
    df_clean["calories"] = (
        df_clean["calories"]
        .fillna(300)
        .round(0)
        .astype(int)
    )
    df_clean["heart_rate"] = (
        df_clean["heart_rate"]
        .fillna(70)
        .round(0)
        .astype(int)
    )
    df_clean["goal"] = df_clean["goal"].str.lower().str.strip()
    print("  ✅ Types de données corrigés")

    # 10. SAVE CLEAN DATA
    df_clean.to_csv("data/clean_data.csv", index=False)
    df_clean.to_json(
        "data/clean_data.json",
        orient="records",
        indent=2,
        date_format="iso"
    )

    # 11. FINAL REPORT
    missing_after = df_clean.isnull().sum().sum()
    report["missing_after"] = int(missing_after)
    print(f"  ✅ Valeurs manquantes : {missing_before} → {missing_after}")

    return df_clean, report


def run_full_pipeline(n_users=50, n_days=30):
    """
    Execute le pipeline complet :
    1. Collecte des donnees brutes
    2. Nettoyage et preprocessing
    """
    print("\n  🚀  Démarrage du pipeline...\n")

    # Étape 1 : Collecte
    df_raw = collect_raw_data(n_users=n_users, n_days=n_days)

    # Étape 2 : Nettoyage
    print("\n  🧹  Nettoyage des données...\n")
    df_clean, report = clean_data(df_raw)

    print(f"\n  ✅  Pipeline terminé !")
    print(f"       Lignes finales : {df_clean.shape[0]}")

    return df_clean, report