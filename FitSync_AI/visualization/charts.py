import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. GRAPHIQUE LINÉAIRE (Time Series)
def plot_steps_calories(df):
    """Affiche la progression des pas et calories au fil du temps."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    
    daily = df.groupby("date")[["steps", "calories"]].mean().reset_index()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    sns.lineplot(data=daily, x="date", y="steps", ax=ax1, color="blue", marker="o")
    ax1.set_title("Évolution des Pas")
    
    sns.lineplot(data=daily, x="date", y="calories", ax=ax2, color="red", marker="o")
    ax2.set_title("Évolution des Calories")
    
    plt.tight_layout()
    plt.savefig("visualization/steps_calories.png")
    plt.show()

# 2. GRAPHIQUE À BARRES (Bar Chart)
def plot_workout_frequency(df):
    """Compte combien de séances pour chaque type de sport."""
    plt.figure(figsize=(10, 6))
    workout_counts = df["workout"].value_counts()
    
    # Correction : ajout de hue=workout_counts.index et legend=False
    sns.barplot(x=workout_counts.index, y=workout_counts.values, hue=workout_counts.index, palette="viridis", legend=False)
    
    plt.title("🏋️ Fréquence des types d'entraînement")
    plt.show()

# 3. BOXPLOT (Boîte à moustaches)
def plot_calories_by_workout(df):
    """Montre la distribution des calories par sport."""
    plt.figure(figsize=(10, 6))
    
    # Correction : ajout de hue="workout" et legend=False
    sns.boxplot(data=df, x="workout", y="calories", hue="workout", palette="Set2", legend=False)
    
    plt.title("Distribution des Calories par type d'entraînement")
    plt.show()

# 4. CAMEMBERT (Pie Chart)
def plot_goals_distribution(df):
    """Répartition des objectifs des utilisateurs."""
    plt.figure(figsize=(8, 8))
    goal_counts = df.groupby("goal")["name"].nunique()
    
    plt.pie(goal_counts.values, labels=goal_counts.index, autopct="%1.1f%%")
    plt.title("Répartition des objectifs des utilisateurs")
    plt.show()