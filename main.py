import os
import sys
from models.user import generate_fake_users
from models.workout import Workout
from utils.file_manager import save_users, load_users
from utils.weather import get_weather, display_weather
from utils.weekly_report import generate_weekly_report
from utils.badges import check_badges, ALL_BADGES
from analysis.stats import full_statistical_analysis
from visualization.charts import generate_all_charts
from data.pipeline import run_full_pipeline


def clear_screen():
    """Nettoie le terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Affiche le header de l'application"""
    print("\n" + "═" * 50)
    print("║" + " " * 14 + "🏋️  FitSync AI  💪" + " " * 14 + "║")
    print("║" + " " * 10 +
          "Votre Coach Fitness Intelligent" +
          " " * 8 + "║")
    print("║" + " " * 12 +
          "Hackathon #1 — COT_GenAI 2026" +
          " " * 8 + "║")
    print("═" * 50)


def print_menu():
    """Affiche le menu principal"""
    print_header()
    print("""
╔══════════════════════════════════════════════╗
║            MENU PRINCIPAL                   ║
╠══════════════════════════════════════════════╣
║  0. 🔬 Pipeline de données complet          ║
║  1. 👤 Générer des profils utilisateurs     ║
║  2. 💪 Plans d'entraînement du jour         ║
║  3. 🌤️  Météo & Recommandation              ║
║  4. 🤖 Voir les FitScores                   ║
║  5. 📊 Analyse statistique complète         ║
║  6. 📈 Générer les graphiques               ║
║  7. 📅 Rapport hebdomadaire                 ║
║  8. 🏅 Système de badges                    ║
║  9. ❌ Quitter                              ║
╚══════════════════════════════════════════════╝
""")


def option_0_pipeline():
    """Lance le pipeline de données complet"""
    print("\n🔬 PIPELINE DE DONNÉES COMPLET")
    print("━" * 45)
    print("Collecte → Nettoyage → Prétraitement\n")

    confirm = input(
        "⚠️  Cela va générer ~1500 lignes "
        "de données. Continuer ? (o/n) : "
    )
    if confirm.lower() != "o":
        print("❌ Pipeline annulé")
        return

    df_processed, report = run_full_pipeline(
        n_users=50, n_days=30
    )

    print("\n📋 Rapport de nettoyage :")
    for key, val in report.items():
        print(f"   {key} : {val}")


def option_1_generate():
    """Génère et sauvegarde des utilisateurs"""
    print("\n👤 GÉNÉRATION DES PROFILS")
    print("━" * 45)

    try:
        n = int(input(
            "Combien d'utilisateurs ? (défaut: 5) : "
        ) or "5")
    except ValueError:
        n = 5

    print(f"\n🔄 Génération de {n} profils...")
    users = generate_fake_users(n)
    save_users(users)

    print(f"\n✅ {n} profils générés :")
    for user in users:
        print(f"   {user}")


def option_2_workout():
    """Génère les plans d'entraînement"""
    print("\n💪 PLANS D'ENTRAÎNEMENT")
    print("━" * 45)

    users_data = load_users()
    if not users_data:
        print("⚠️ Aucun utilisateur trouvé.")
        print("   Lancez l'option 1 d'abord.")
        return

    # Récupérer météo
    weather = get_weather()

    print(f"\n🌤️ Météo du jour : "
          f"{weather['icon']} "
          f"{weather['description']} "
          f"({weather['temperature']}°C)\n")

    from models.user import User
    for user_dict in users_data:
        user = User(
            name=user_dict["name"],
            age=user_dict["age"],
            goal=user_dict["goal"]
        )
        user.daily_logs = user_dict["daily_logs"]
        workout = Workout(user)
        workout.generate_plan(
            weather_condition=weather["condition"]
        )


def option_3_weather():
    """Affiche la météo détaillée"""
    print("\n🌤️ MÉTÉO & RECOMMANDATION")
    print("━" * 45)

    weather = get_weather()
    display_weather(weather)
    print(f"\n💡 Conseil fitness :")
    print(f"   {weather['recommendation']}")


def option_4_fitscore():
    """Affiche les FitScores de tous les users"""
    print("\n🤖 FITSCORES")
    print("━" * 45)

    users_data = load_users()
    if not users_data:
        print("⚠️ Aucun utilisateur trouvé.")
        print("   Lancez l'option 1 d'abord.")
        return

    from models.user import User
    scores = []
    for user_dict in users_data:
        user = User(
            name=user_dict["name"],
            age=user_dict["age"],
            goal=user_dict["goal"]
        )
        user.daily_logs = user_dict["daily_logs"]
        workout = Workout(user)
        score, message = workout.calculate_fit_score()
        scores.append((user.name, score, message))

    # Trier par score décroissant
    scores.sort(key=lambda x: x[1], reverse=True)

    print("\n🏆 CLASSEMENT FITSCORE :")
    print(f"{'─'*45}")
    for i, (name, score, msg) in enumerate(scores, 1):
        bar = "█" * (score // 10) + "░" * (
            10 - score // 10
        )
        print(
            f"  {i}. {name[:20]:<20} "
            f"{bar} {score}/100"
        )
        print(f"     {msg}")
    print(f"{'─'*45}")


def option_5_stats():
    """Lance l'analyse statistique complète"""
    print("\n📊 ANALYSE STATISTIQUE")
    print("━" * 45)

    users_data = load_users()
    if not users_data:
        print("⚠️ Aucun utilisateur trouvé.")
        print("   Lancez l'option 1 d'abord.")
        return

    results = full_statistical_analysis(users_data)
    print("\n✅ Analyse statistique terminée !")


def option_6_charts():
    """Génère tous les graphiques"""
    print("\n📈 GÉNÉRATION DES GRAPHIQUES")
    print("━" * 45)

    users_data = load_users()
    if not users_data:
        print("⚠️ Aucun utilisateur trouvé.")
        print("   Lancez l'option 1 d'abord.")
        return

    generate_all_charts(users_data)
    print("\n✅ Graphiques sauvegardés dans "
          "visualization/")


def option_7_report():
    """Génère les rapports hebdomadaires"""
    print("\n📅 RAPPORTS HEBDOMADAIRES")
    print("━" * 45)

    users_data = load_users()
    if not users_data:
        print("⚠️ Aucun utilisateur trouvé.")
        print("   Lancez l'option 1 d'abord.")
        return

    print("Choisir un utilisateur :")
    for i, u in enumerate(users_data, 1):
        print(f"  {i}. {u['name']}")
    print(f"  0. Tous les utilisateurs")

    try:
        choice = int(input("\nVotre choix : ") or "0")
    except ValueError:
        choice = 0

    if choice == 0:
        for user in users_data:
            generate_weekly_report(user)
    elif 1 <= choice <= len(users_data):
        generate_weekly_report(users_data[choice - 1])
    else:
        print("❌ Choix invalide")


def option_8_badges():
    """Affiche les badges des utilisateurs"""
    print("\n🏅 SYSTÈME DE BADGES")
    print("━" * 45)

    users_data = load_users()
    if not users_data:
        print("⚠️ Aucun utilisateur trouvé.")
        print("   Lancez l'option 1 d'abord.")
        return

    print("Choisir un utilisateur :")
    for i, u in enumerate(users_data, 1):
        print(f"  {i}. {u['name']}")
    print(f"  0. Tous les utilisateurs")

    try:
        choice = int(input("\nVotre choix : ") or "0")
    except ValueError:
        choice = 0

    from models.user import User
    if choice == 0:
        for user_dict in users_data:
            user = User(
                name=user_dict["name"],
                age=user_dict["age"],
                goal=user_dict["goal"]
            )
            user.daily_logs = user_dict["daily_logs"]
            workout = Workout(user)
            score, _ = workout.calculate_fit_score()
            check_badges(user_dict, score)
    elif 1 <= choice <= len(users_data):
        user_dict = users_data[choice - 1]
        user = User(
            name=user_dict["name"],
            age=user_dict["age"],
            goal=user_dict["goal"]
        )
        user.daily_logs = user_dict["daily_logs"]
        workout = Workout(user)
        score, _ = workout.calculate_fit_score()
        check_badges(user_dict, score)
    else:
        print("❌ Choix invalide")


def main():
    """Point d'entrée principal — Menu interactif"""

    OPTIONS = {
        "0": option_0_pipeline,
        "1": option_1_generate,
        "2": option_2_workout,
        "3": option_3_weather,
        "4": option_4_fitscore,
        "5": option_5_stats,
        "6": option_6_charts,
        "7": option_7_report,
        "8": option_8_badges,
    }

    while True:
        print_menu()
        choice = input("👉 Votre choix : ").strip()

        if choice == "9":
            print(
                "\n👋 À bientôt sur FitSync AI !"
            )
            print(
                "   FitSync Masters — "
                "Rabiatou & Dia Oumar 💪\n"
            )
            sys.exit(0)

        elif choice in OPTIONS:
            try:
                OPTIONS[choice]()
            except Exception as e:
                print(f"\n❌ Erreur : {e}")

            input("\n⏎  Appuyez sur Entrée "
                  "pour continuer...")
        else:
            print(
                "\n❌ Option invalide. "
                "Choisissez entre 0 et 9."
            )
            input("\n⏎  Appuyez sur Entrée "
                  "pour continuer...")


if __name__ == "__main__":
    main()