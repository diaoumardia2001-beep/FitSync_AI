import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import subprocess

# ❌ IMPORTANT : on supprime Agg pour permettre les fenêtres
# matplotlib.use('Agg')  ← SUPPRIMÉ

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


# =========================
# DATA PREPARATION
# =========================
def prepare_df(users):
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


# =========================
# GRAPH 1
# =========================
def plot_steps_calories(users):
    df = prepare_df(users)

    daily = df.groupby("date")[["steps", "calories"]].mean().reset_index()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

    fig.suptitle(
        "Progression Quotidienne — FitSync AI",
        fontsize=16, fontweight="bold", color="white"
    )

    # Steps
    ax1.plot(daily["date"], daily["steps"], color=COLORS[0], marker="o")
    ax1.set_title("Pas par jour")
    ax1.tick_params(axis="x", rotation=45)

    # Calories
    ax2.plot(daily["date"], daily["calories"], color=COLORS[1], marker="o")
    ax2.set_title("Calories par jour")
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout()

    path = "visualization/steps_calories.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")

    plt.show()   # ✅ OUVRE LA FENÊTRE
    plt.close()

    print(f"  ✅ Sauvegarde : {path}")
    return path


# =========================
# GRAPH 2
# =========================
def plot_workout_frequency(users):
    df = prepare_df(users)
    workout_counts = df["workout"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(workout_counts.index, workout_counts.values, color=COLORS[0])

    ax.set_title("Fréquence des workouts")
    ax.tick_params(axis="x", rotation=45)

    path = "visualization/workout_frequency.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")

    plt.show()
    plt.close()

    print(f"  ✅ Sauvegarde : {path}")
    return path


# =========================
# GRAPH 3
# =========================
def plot_calories_by_workout(users):
    df = prepare_df(users)

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.boxplot(data=df, x="workout", y="calories", ax=ax)

    ax.set_title("Calories par workout")
    ax.tick_params(axis="x", rotation=45)

    path = "visualization/calories_by_workout.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")

    plt.show()
    plt.close()

    print(f"  ✅ Sauvegarde : {path}")
    return path


# =========================
# GRAPH 4
# =========================
def plot_goals_distribution(users):
    df = prepare_df(users)
    goal_counts = df["goal"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.pie(goal_counts.values, labels=goal_counts.index, autopct="%1.1f%%")

    ax.set_title("Objectifs fitness")

    path = "visualization/goals_distribution.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")

    plt.show()
    plt.close()

    print(f"  ✅ Sauvegarde : {path}")
    return path


# =========================
# OPEN IMAGE (OPTIONAL)
# =========================
def open_image(path):
    try:
        if os.name == "nt":
            os.startfile(os.path.abspath(path))
        elif os.name == "posix":
            subprocess.call(["xdg-open", path])
    except Exception as e:
        print("Erreur ouverture image:", e)


# =========================
# MAIN FUNCTION
# =========================
def generate_all_charts(users):
    print("\n📊 Génération des graphiques...\n")

    paths = [
        plot_steps_calories(users),
        plot_workout_frequency(users),
        plot_calories_by_workout(users),
        plot_goals_distribution(users)
    ]

    print("\n✅ Tous les graphiques générés !")

    for p in paths:
        if os.path.exists(p):
            open_image(p)
            