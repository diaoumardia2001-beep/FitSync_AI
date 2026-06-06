import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_steps_calories(df):
    """Graphique linéaire : pas et calories au fil du temps"""
    
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    
    # Grouper par date
    daily = df.groupby("date")[["steps", "calories"]].mean().reset_index()
    daily = daily.sort_values("date")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle("📈 Progression quotidienne", fontsize=16, fontweight="bold")

    # Graphique des pas
    sns.lineplot(data=daily, x="date", y="steps", ax=ax1, color="blue", marker="o")
    ax1.set_title("👟 Nombre de pas par jour")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Pas")
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)

    # Graphique des calories
    sns.lineplot(data=daily, x="date", y="calories", ax=ax2, color="red", marker="o")
    ax2.set_title("🔥 Calories brûlées par jour")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Calories")
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("visualization/steps_calories.png")
    plt.show()
    print("✅ Graphique sauvegardé : visualization/steps_calories.png")


def plot_workout_frequency(df):
    """Graphique à barres : fréquence des types de workout"""

    plt.figure(figsize=(10, 6))
    workout_counts = df["workout"].value_counts()

    sns.barplot(x=workout_counts.index, y=workout_counts.values, palette="viridis")
    plt.title("🏋️ Fréquence des types d'entraînement", fontsize=14, fontweight="bold")
    plt.xlabel("Type de workout")
    plt.ylabel("Nombre de séances")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("visualization/workout_frequency.png")
    plt.show()
    print("✅ Graphique sauvegardé : visualization/workout_frequency.png")


def plot_calories_by_workout(df):
    """Boxplot : distribution des calories par type de workout"""

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="workout", y="calories", palette="Set2")
    plt.title("📊 Calories brûlées par type de workout", fontsize=14, fontweight="bold")
    plt.xlabel("Type de workout")
    plt.ylabel("Calories")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("visualization/calories_by_workout.png")
    plt.show()
    print("✅ Graphique sauvegardé : visualization/calories_by_workout.png")


def plot_goals_distribution(df):
    """Camembert : distribution des objectifs"""

    plt.figure(figsize=(8, 8))
    goal_counts = df.groupby("goal")["name"].nunique()

    plt.pie(
        goal_counts.values,
        labels=goal_counts.index,
        autopct="%1.1f%%",
        colors=sns.color_palette("pastel")
    )
    plt.title("🎯 Distribution des objectifs fitness", fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.savefig("visualization/goals_distribution.png")
    plt.show()
    print("✅ Graphique sauvegardé : visualization/goals_distribution.png")