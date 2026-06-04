from models.user import generate_fake_users
from models.workout import Workout
from utils.file_manager import save_users, load_users
from analysis.stats import prepare_dataframe, anova_calories_by_workout, linear_regression_steps, ttest_before_after
from visualization.charts import plot_steps_calories, plot_workout_frequency, plot_calories_by_workout, plot_goals_distribution

def main():
    print("🏋️ Bienvenue sur FitSync AI !\n")

    # Générer les utilisateurs
    print("📋 Génération des utilisateurs...")
    users = generate_fake_users(5)
    save_users(users)

    # Plans d'entraînement
    print("\n💪 Plans d'entraînement personnalisés :")
    print("=" * 50)
    for user in users:
        workout = Workout(user)
        workout.generate_plan()

    # Analyse SciPy
    print("\n🔬 Analyse statistique :")
    df = prepare_dataframe(users)
    anova_calories_by_workout(df)
    linear_regression_steps(df)
    ttest_before_after(df)

    # Visualisations
    print("\n📊 Génération des graphiques...")
    plot_steps_calories(df)
    plot_workout_frequency(df)
    plot_calories_by_workout(df)
    plot_goals_distribution(df)

if __name__ == "__main__":
    main()