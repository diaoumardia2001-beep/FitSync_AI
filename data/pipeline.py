import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from functools import reduce

fake = Faker()

GOALS = ["weight_loss", "strength", "cardio", "flexibility"]
WORKOUTS = [
    "Yoga", "Running", "HIIT",
    "Strength Training", "Cycling", "Walking"
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉTAPE 1 — COLLECTE DES DONNÉES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def collect_raw_data(n_users=50, n_days=30):
    """
    Génère un dataset brut RÉALISTE avec Faker
    Contient intentionnellement des imperfections :
    - Valeurs manquantes
    - Doublons
    - Outliers
    - Valeurs impossibles
    """
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

            # Valeurs manquantes (15% de chance)
            steps = (
                random.randint(1000, 20000)
                if random.random() > 0.15
                else None
            )

            # Calories avec outliers
            cal_type = random.random()
            if cal_type < 0.70:
                calories = random.randint(150, 700)
            elif cal_type < 0.85:
                calories = random.randint(1500, 3000)
            elif cal_type < 0.92:
                calories = -random.randint(10, 100)
            else:
                calories = None

            # Workout avec données sales
            workout = random.choice(
                WORKOUTS + [None, "", "  "]
            )

            # Heart rate avec valeurs impossibles
            hr_type = random.random()
            if hr_type < 0.75:
                heart_rate = random.randint(60, 180)
            elif hr_type < 0.90:
                heart_rate = random.randint(300, 500)
            else:
                heart_rate = None

            # Sleep hours
            sleep_type = random.random()
            if sleep_type < 0.75:
                sleep_hours = round(
                    random.uniform(4, 10), 1
                )
            elif sleep_type < 0.90:
                sleep_hours = round(
                    random.uniform(20, 30), 1
                )
            else:
                sleep_hours = None

            # Poids
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

            # Doublons intentionnels (5%)
            if random.random() < 0.05:
                rows.append(row.copy())

    df = pd.DataFrame(rows)

    # Sauvegarde
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_data.csv", index=False)
    df.to_json(
        "data/raw_data.json",
        orient="records",
        indent=2
    )

    print(f"\n📥 COLLECTE TERMINÉE")
    print(f"   Lignes totales    : {len(df)}")
    print(
        f"   Valeurs manquantes: "
        f"{df.isnull().sum().sum()}"
    )
    print(f"   Doublons          : {df.duplicated().sum()}")

    return df


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉTAPE 2 — NETTOYAGE DES DONNÉES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def clean_data(df):
    """
    Pipeline complet de nettoyage :
    - Valeurs manquantes
    - Doublons
    - Outliers (méthode IQR)
    - Valeurs impossibles
    - Types de données
    """
    report = {}
    df_clean = df.copy()

    print(f"\n🧹 NETTOYAGE DES DONNÉES")
    print("━" * 40)

    # 1. VALEURS MANQUANTES
    missing_before = df_clean.isnull().sum().sum()
    report["missing_before"] = int(missing_before)

    # Steps → médiane par objectif
    df_clean["steps"] = df_clean.groupby(
        "goal"
    )["steps"].transform(
        lambda x: x.fillna(x.median())
    )

    # Calories → médiane par workout
    df_clean["calories"] = df_clean.groupby(
        "workout"
    )["calories"].transform(
        lambda x: x.fillna(x.median())
    )

    # Heart rate → médiane globale
    df_clean["heart_rate"] = df_clean[
        "heart_rate"
    ].fillna(df_clean["heart_rate"].median())

    # Sleep hours → médiane globale
    df_clean["sleep_hours"] = df_clean[
        "sleep_hours"
    ].fillna(df_clean["sleep_hours"].median())

    # Weight → médiane globale
    df_clean["weight_kg"] = df_clean[
        "weight_kg"
    ].fillna(df_clean["weight_kg"].median())

    # Workout vide → "Unknown"
    df_clean["workout"] = df_clean["workout"].replace(
        ["", "  ", None], "Unknown"
    )
    df_clean["workout"] = df_clean[
        "workout"
    ].fillna("Unknown")

    missing_after = df_clean.isnull().sum().sum()
    report["missing_after"] = int(missing_after)

    print(
        f"✅ Valeurs manquantes : "
        f"{missing_before} → {missing_after}"
    )

    # 2. DOUBLONS
    dupl_before = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    dupl_after = df_clean.duplicated().sum()
    report["duplicates_removed"] = int(
        dupl_before - dupl_after
    )
    print(
        f"✅ Doublons supprimés : "
        f"{dupl_before - dupl_after}"
    )

    # 3. OUTLIERS — Méthode IQR
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
    for col in ["steps", "calories",
                "heart_rate", "sleep_hours"]:
        df_clean, n = remove_outliers_iqr(df_clean, col)
        report[f"outliers_{col}"] = n
        total_outliers += n

    print(f"✅ Outliers traités   : {total_outliers}")

    # 4. VALEURS IMPOSSIBLES
    # Calories négatives
    neg_cal = (df_clean["calories"] < 0).sum()
    df_clean.loc[
        df_clean["calories"] < 0, "calories"
    ] = df_clean["calories"].median()

    # Heart rate impossible
    df_clean.loc[
        df_clean["heart_rate"] > 220, "heart_rate"
    ] = 100
    df_clean.loc[
        df_clean["heart_rate"] < 40, "heart_rate"
    ] = 60

    # Sleep hours impossible
    df_clean.loc[
        df_clean["sleep_hours"] > 14, "sleep_hours"
    ] = 7.0

    # Steps négatifs
    df_clean.loc[
        df_clean["steps"] < 0, "steps"
    ] = 0

    report["impossible_values"] = int(neg_cal)
    print(f"✅ Valeurs impossibles: {neg_cal} corrigées")

    # 5. TYPES DE DONNÉES
    df_clean["date"] = pd.to_datetime(df_clean["date"])
    df_clean["age"] = df_clean["age"].astype(int)
    df_clean["steps"] = df_clean["steps"].astype(int)
    df_clean["calories"] = df_clean[
        "calories"
    ].astype(int)
    df_clean["workout"] = df_clean[
        "workout"
    ].str.strip()
    df_clean["goal"] = df_clean[
        "goal"
    ].str.lower().str.strip()

    print(f"✅ Types de données corrigés")

    # Sauvegarde
    df_clean.to_csv("data/clean_data.csv", index=False)
    df_clean.to_json(
        "data/clean_data.json",
        orient="records",
        indent=2,
        date_format="iso"
    )

    print(f"\n📊 Dataset nettoyé   : {df_clean.shape}")
    return df_clean, report


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉTAPE 3 — PRÉTRAITEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def preprocess_data(df_clean):
    """
    Prétraitement complet :
    - Normalisation Min-Max
    - Standardisation Z-score
    - Encodage variables catégoriques
    - Feature Engineering
    - Lambda, Map, Filter, Reduce
    """
    df = df_clean.copy()

    print(f"\n⚙️  PRÉTRAITEMENT")
    print("━" * 40)

    NUMERIC_COLS = [
        "steps", "calories",
        "heart_rate", "sleep_hours"
    ]

    # 1. NORMALISATION MIN-MAX
    df_normalized = df.copy()
    for col in NUMERIC_COLS:
        col_min = df[col].min()
        col_max = df[col].max()
        df_normalized[f"{col}_normalized"] = (
            (df[col] - col_min) / (col_max - col_min)
        ).round(4)

    print("✅ Normalisation Min-Max appliquée")

    # 2. STANDARDISATION Z-SCORE
    df_standardized = df.copy()
    for col in NUMERIC_COLS:
        mean = df[col].mean()
        std = df[col].std()
        df_standardized[f"{col}_zscore"] = (
            (df[col] - mean) / std
        ).round(4)

    print("✅ Standardisation Z-score appliquée")

    # 3. ENCODAGE — MAP (cours)
    goal_encoding = {
        "weight_loss": 0,
        "strength": 1,
        "cardio": 2,
        "flexibility": 3
    }
    workout_encoding = {
        "Yoga": 0, "Running": 1,
        "HIIT": 2, "Strength Training": 3,
        "Cycling": 4, "Walking": 5,
        "Unknown": 6
    }

    df["goal_encoded"] = df["goal"].map(goal_encoding)
    df["workout_encoded"] = df["workout"].map(
        workout_encoding
    ).fillna(6).astype(int)

    print("✅ Encodage des variables catégoriques")

    # 4. FEATURE ENGINEERING

    # Niveau d'activité — LAMBDA (cours)
    activity_level = lambda steps: (
        "faible" if steps < 5000
        else "moyen" if steps < 10000
        else "élevé"
    )
    df["activity_level"] = df["steps"].apply(
        activity_level
    )

    # Efficacité calorique
    df["calorie_efficiency"] = (
        df["calories"] / df["steps"].replace(0, 1)
    ).round(4)

    # Semaine de l'année
    df["week_number"] = df["date"].dt.isocalendar(
    ).week.astype(int)

    # Jour de la semaine
    df["day_of_week"] = df["date"].dt.day_name()

    # Score fitness brut
    df["raw_fitness_score"] = (
        df["steps"] * 0.4 +
        df["calories"] * 0.6
    ).round(2)

    # IMC approximatif
    df["bmi_approx"] = (
        df["weight_kg"] / ((1.70) ** 2)
    ).round(1)

    print("✅ Feature Engineering terminé")

    # 5. FILTER (cours) — utilisateurs actifs
    active_steps = list(filter(
        lambda x: x > 5000,
        df["steps"].tolist()
    ))
    print(
        f"✅ Jours actifs filtrés  : "
        f"{len(active_steps)}"
    )

    # 6. REDUCE (cours) — total calories
    total_cal = reduce(
        lambda x, y: x + y,
        df["calories"].tolist()
    )
    print(
        f"✅ Total calories (reduce): "
        f"{total_cal:,}"
    )

    # Résumé statistique
    print(f"\n📊 Résumé statistique :")
    print(df[NUMERIC_COLS].describe().round(2))

    # Sauvegarde
    df.to_csv(
        "data/preprocessed_data.csv",
        index=False
    )
    df.to_json(
        "data/preprocessed_data.json",
        orient="records",
        indent=2,
        date_format="iso"
    )

    return df, df_normalized, df_standardized


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PIPELINE PRINCIPAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_full_pipeline(n_users=50, n_days=30):
    """
    Lance le pipeline complet :
    Collecte → Nettoyage → Prétraitement
    """
    print("🚀 PIPELINE DE DONNÉES FITSYNC AI")
    print("━" * 40)

    # Étape 1
    df_raw = collect_raw_data(n_users, n_days)

    # Étape 2
    df_clean, cleaning_report = clean_data(df_raw)

    # Étape 3
    df_processed, df_norm, df_std = preprocess_data(
        df_clean
    )

    print(f"\n✅ PIPELINE TERMINÉ !")
    print(f"   raw_data         : {df_raw.shape}")
    print(f"   clean_data       : {df_clean.shape}")
    print(f"   preprocessed     : {df_processed.shape}")
    print(f"\n📁 Fichiers sauvegardés dans data/")

    return df_processed, cleaning_report