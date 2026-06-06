import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Style global
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#16213e",
    "axes.labelcolor": "white",
    "text.color": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#2d2d5e",
    "font.family": "sans-serif"
})

COLORS = [
    "#00D4FF", "#00FF88", "#FFD700",
    "#FF6B6B", "#8B5CF6", "#FF8C00"
]

os.makedirs("visualization", exist_ok=True)


def prepare_df(users):
    """
    Convertit les utilisateurs en DataFrame
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
    return df.sort_values("date")


def plot_steps_calories(users):
    """
    Graphique linéaire double :
    Évolution des pas et calories au fil du temps
    """
    df = prepare_df(users)
    daily = df.groupby("date")[
        ["steps", "calories"]
    ].mean().reset_index()

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(14, 8)
    )
    fig.suptitle(
        "📈 Progression Quotidienne — FitSync AI",
        fontsize=16,
        fontweight="bold",
        color="white"
    )

    # Graphique des pas
    ax1.plot(
        daily["date"], daily["steps"],
        color=COLORS[0],
        linewidth=2.5,
        marker="o",
        markersize=4,
        label="Pas moyens"
    )
    ax1.fill_between(
        daily["date"], daily["steps"],
        alpha=0.15,
        color=COLORS[0]
    )
    ax1.set_title(
        "👟 Nombre de pas par jour",
        color="white",
        fontsize=13
    )
    ax1.set_ylabel("Pas", color="white")
    ax1.legend(facecolor="#16213e", labelcolor="white")
    ax1.tick_params(axis="x", rotation=45)

    # Graphique des calories
    ax2.plot(
        daily["date"], daily["calories"],
        color=COLORS[1],
        linewidth=2.5,
        marker="o",
        markersize=4,
        label="Calories moyennes"
    )
    ax2.fill_between(
        daily["date"], daily["calories"],
        alpha=0.15,
        color=COLORS[1]
    )
    ax2.set_title(
        "🔥 Calories brûlées par jour",
        color="white",
        fontsize=13
    )
    ax2.set_ylabel("Calories", color="white")
    ax2.set_xlabel("Date", color="white")
    ax2.legend(facecolor="#16213e", labelcolor="white")
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    path = "visualization/steps_calories.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ Graphique sauvegardé : {path}")


def plot_workout_frequency(users):
    """
    Graphique à barres horizontal :
    Fréquence des types de workout
    """
    df = prepare_df(users)
    workout_counts = df["workout"].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle(
        "🏋️ Fréquence des Entraînements",
        fontsize=16,
        fontweight="bold",
        color="white"
    )

    bars = ax.barh(
        workout_counts.index,
        workout_counts.values,
        color=COLORS[:len(workout_counts)],
        edgecolor="none",
        height=0.6
    )

    # Labels sur les barres
    for bar, val in zip(bars, workout_counts.values):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{val}",
            va="center",
            color="white",
            fontweight="bold"
        )

    ax.set_xlabel("Nombre de séances", color="white")
    ax.set_title(
        "Types d'entraînement pratiqués",
        color="white"
    )
    ax.invert_yaxis()

    plt.tight_layout()
    path = "visualization/workout_frequency.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ Graphique sauvegardé : {path}")


def plot_calories_by_workout(users):
    """
    Boxplot : Distribution des calories
    par type de workout
    """
    df = prepare_df(users)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle(
        "📊 Distribution des Calories par Workout",
        fontsize=16,
        fontweight="bold",
        color="white"
    )

    sns.boxplot(
        data=df,
        x="workout",
        y="calories",
        palette=COLORS,
        ax=ax,
        linewidth=1.5
    )

    ax.set_xlabel("Type de workout", color="white")
    ax.set_ylabel("Calories", color="white")
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    path = "visualization/calories_by_workout.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ Graphique sauvegardé : {path}")


def plot_goals_distribution(users):
    """
    Camembert : Répartition des objectifs fitness
    """
    df = prepare_df(users)
    goal_counts = df.groupby("goal")["name"].nunique()

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.suptitle(
        "🎯 Distribution des Objectifs Fitness",
        fontsize=16,
        fontweight="bold",
        color="white"
    )

    wedges, texts, autotexts = ax.pie(
        goal_counts.values,
        labels=goal_counts.index,
        autopct="%1.1f%%",
        colors=COLORS[:len(goal_counts)],
        startangle=90,
        wedgeprops={"edgecolor": "#1a1a2e", "linewidth": 2}
    )

    for text in texts:
        text.set_color("white")
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    plt.tight_layout()
    path = "visualization/goals_distribution.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ Graphique sauvegardé : {path}")


def plot_cleaning_report(df_raw, df_clean):
    """
    Graphiques avant/après nettoyage des données
    Montre l'impact du pipeline de nettoyage
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(
        "🧹 Rapport de Nettoyage des Données",
        fontsize=16,
        fontweight="bold",
        color="white"
    )

    # 1. Valeurs manquantes avant/après
    missing_before = df_raw.isnull().sum()
    missing_after = df_clean.isnull().sum()
    x = range(len(missing_before))

    axes[0, 0].bar(
        x, missing_before.values,
        alpha=0.7, color="#FF6B6B",
        label="Avant"
    )
    axes[0, 0].bar(
        x, missing_after.values,
        alpha=0.7, color="#00FF88",
        label="Après"
    )
    axes[0, 0].set_xticks(list(x))
    axes[0, 0].set_xticklabels(
        missing_before.index, rotation=45
    )
    axes[0, 0].set_title(
        "Valeurs manquantes", color="white"
    )
    axes[0, 0].legend(
        facecolor="#16213e",
        labelcolor="white"
    )

    # 2. Distribution steps avant/après
    axes[0, 1].hist(
        df_raw["steps"].dropna(),
        bins=30, alpha=0.6,
        color="#FF6B6B", label="Avant"
    )
    axes[0, 1].hist(
        df_clean["steps"].dropna(),
        bins=30, alpha=0.6,
        color="#00FF88", label="Après"
    )
    axes[0, 1].set_title(
        "Distribution des pas", color="white"
    )
    axes[0, 1].legend(
        facecolor="#16213e",
        labelcolor="white"
    )

    # 3. Boxplot calories avant/après
    axes[0, 2].boxplot(
        [
            df_raw["calories"].dropna(),
            df_clean["calories"].dropna()
        ],
        labels=["Avant", "Après"],
        patch_artist=True,
        boxprops=dict(facecolor="#16213e"),
        medianprops=dict(color="#00D4FF")
    )
    axes[0, 2].set_title(
        "Outliers calories", color="white"
    )

    # 4. Heatmap corrélations
    corr_cols = [
        "steps", "calories",
        "heart_rate", "sleep_hours", "age"
    ]
    corr = df_clean[corr_cols].corr()
    sns.heatmap(
        corr, annot=True, fmt=".2f",
        cmap="coolwarm",
        ax=axes[1, 0],
        linewidths=0.5,
        annot_kws={"color": "white"}
    )
    axes[1, 0].set_title(
        "Matrice de corrélation", color="white"
    )

    # 5. Distribution objectifs
    goal_counts = df_clean["goal"].value_counts()
    axes[1, 1].pie(
        goal_counts.values,
        labels=goal_counts.index,
        autopct="%1.1f%%",
        colors=COLORS[:len(goal_counts)]
    )
    axes[1, 1].set_title(
        "Répartition objectifs", color="white"
    )

    # 6. Niveaux d'activité
    activity_level = lambda s: (
        "faible" if s < 5000
        else "moyen" if s < 10000
        else "élevé"
    )
    df_clean["activity"] = df_clean["steps"].apply(
        activity_level
    )
    activity_counts = df_clean["activity"].value_counts()

    sns.barplot(
        x=activity_counts.index,
        y=activity_counts.values,
        palette=COLORS[:3],
        ax=axes[1, 2]
    )
    axes[1, 2].set_title(
        "Niveaux d'activité", color="white"
    )

    plt.tight_layout()
    path = "visualization/cleaning_report.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✅ Rapport nettoyage sauvegardé : {path}")


def generate_all_charts(users):
    """
    Génère tous les graphiques d'un coup
    """
    print("\n📊 Génération des graphiques...")
    plot_steps_calories(users)
    plot_workout_frequency(users)
    plot_calories_by_workout(users)
    plot_goals_distribution(users)
    print("\n✅ Tous les graphiques générés !")