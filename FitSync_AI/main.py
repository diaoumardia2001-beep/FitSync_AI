# Importation des modules : on rassemble ici les briques que nous avons créées
from models.user import generate_fake_users
from models.workout import Workout
from utils.file_manager import save_users, load_users
from analysis.stats import prepare_dataframe, anova_calories_by_workout, linear_regression_steps, ttest_before_after
from visualization.charts import plot_steps_calories, plot_workout_frequency, plot_calories_by_workout, plot_goals_distribution

def main():
    """
    Le point d'entrée du programme. 
    L'ordre ici est crucial : on ne peut pas analyser des données qu'on n'a pas encore créées !
    """
    print("🏋️ Bienvenue sur FitSync AI !\n")

    # ÉTAPE 1 : Génération de données (Le moteur de données)
    # On utilise notre classe User pour peupler notre base de données fictive.
    print("📋 Génération des utilisateurs...")
    users = generate_fake_users(5)
    save_users(users) # On rend les données persistantes (sauvegarde sur disque)

    # ÉTAPE 2 : Logique métier (Le moteur de recommandation)
    # On transforme l'utilisateur en objet 'Workout' pour générer des conseils.
    print("\n💪 Plans d'entraînement personnalisés :")
    print("=" * 50)
    for user in users:
        workout = Workout(user)
        workout.generate_plan() # Affiche les recommandations selon les données

    # ÉTAPE 3 : Analyse Statistique (Le moteur mathématique)
    # On transforme les données en DataFrame Pandas pour les analyser en masse.
    print("\n🔬 Analyse statistique :")
    df = prepare_dataframe(users)
    anova_calories_by_workout(df)        # Test de comparaison des groupes
    linear_regression_steps(df)          # Modèle de prédiction future
    ttest_before_after(df)               # Test de précision (Strength vs HIIT)

    # ÉTAPE 4 : Visualisation (Le moteur de communication)
    # Enfin, on traduit les résultats mathématiques en visuels clairs.
    print("\n📊 Génération des graphiques...")
    plot_steps_calories(df)
    plot_workout_frequency(df)
    plot_calories_by_workout(df)
    plot_goals_distribution(df)

# Cette condition vérifie que le script est lancé directement (et non importé)
if __name__ == "__main__":
    main()