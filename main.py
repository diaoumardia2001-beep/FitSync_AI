import os
import sys
import time
from models.user import generate_fake_users, User
from models.workout import Workout
from utils.file_manager import save_users, load_users
from utils.weather import get_weather, display_weather
from utils.weekly_report import generate_weekly_report
from utils.badges import check_badges, ALL_BADGES
from analysis.stats import full_statistical_analysis
from visualization.charts import generate_all_charts
from data.pipeline import run_full_pipeline


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UTILITAIRES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def type_text(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def loading_bar(label="Chargement", duration=1.5):
    bar_len = 30
    print(f"\n  {label} :")
    print("  [", end="", flush=True)
    for i in range(bar_len):
        time.sleep(duration / bar_len)
        print("█", end="", flush=True)
    print("] ✅")


def step_ok(text, delay=0.4):
    time.sleep(delay)
    print(f"  ✅  {text}")


def divider(char="━", length=52):
    print("  " + char * length)


def title(text):
    print()
    divider("═")
    pad = (52 - len(text)) // 2
    print("  ║" + " " * pad + text + " " * (52 - pad - len(text)) + "║")
    divider("═")
    print()


def pause():
    print()
    input("  ⏎  Appuyez sur Entrée pour continuer...")


def ask(prompt):
    return input(f"  👉  {prompt} : ").strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SPLASH SCREEN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def splash_screen():
    clear()
    print()
    logo = """
  ███████╗██╗████████╗███████╗██╗   ██╗███╗   ██╗ ██████╗
  ██╔════╝██║╚══██╔══╝██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝
  █████╗  ██║   ██║   ███████╗ ╚████╔╝ ██╔██╗ ██║██║
  ██╔══╝  ██║   ██║   ╚════██║  ╚██╔╝  ██║╚██╗██║██║
  ██║     ██║   ██║   ███████║   ██║   ██║ ╚████║╚██████╗
  ╚═╝     ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝
    """
    print(logo)
    time.sleep(0.4)
    type_text(
        "        🏋️  Votre Coach Fitness Intelligent",
        delay=0.04
    )
    type_text(
        "        👥  FitSync Masters — Hackathon #1 · COT_GenAI 2026",
        delay=0.03
    )
    time.sleep(0.5)
    print()
    loading_bar("  Démarrage de l'application", 1.2)
    time.sleep(0.5)
    clear()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉTAPE 1 — PIPELINE DE DONNÉES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def etape_1_pipeline():
    clear()
    title("ÉTAPE 1 — PIPELINE DE DONNÉES")

    print("  Ce pipeline va :")
    print()

    steps = [
        ("📥", "Collecter les données brutes avec Faker"),
        ("🔍", "Détecter les valeurs manquantes et doublons"),
        ("🧹", "Nettoyer et corriger les données"),
        ("⚙️ ", "Prétraiter — normalisation + encodage"),
        ("💾", "Sauvegarder en CSV et JSON"),
    ]

    for icon, text in steps:
        time.sleep(0.3)
        print(f"     {icon}  {text}")

    print()
    loading_bar("  Exécution du pipeline", 2.5)

    df_processed, report = run_full_pipeline(
        n_users=50, n_days=30
    )

    print()
    divider()
    print("  📋  RÉSULTATS DU NETTOYAGE")
    divider()
    time.sleep(0.2)
    print(f"     Valeurs manquantes traitées : {report.get('missing_before', 0)}")
    time.sleep(0.2)
    print(f"     Doublons supprimés          : {report.get('duplicates_removed', 0)}")
    time.sleep(0.2)
    total_out = sum(
        v for k, v in report.items()
        if k.startswith("outliers_")
    )
    print(f"     Outliers corrigés           : {total_out}")
    time.sleep(0.2)
    print(f"     Dataset final               : {df_processed.shape[0]} lignes × {df_processed.shape[1]} colonnes")
    divider()

    print()
    step_ok("Pipeline terminé avec succès !")
    time.sleep(0.5)
    pause()

    return df_processed


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉTAPE 2 — GÉNÉRER LES PROFILS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def etape_2_profils():
    clear()
    title("ÉTAPE 2 — GÉNÉRATION DES PROFILS")

    try:
        n = int(ask("Combien d'utilisateurs à générer ? (défaut: 5)") or "5")
    except ValueError:
        n = 5

    print()
    loading_bar(f"  Génération de {n} profils avec Faker", 1.0)

    users = generate_fake_users(n)
    save_users(users)

    print()
    divider()
    print("  👤  PROFILS CRÉÉS")
    divider()

    for i, user in enumerate(users, 1):
        time.sleep(0.25)
        print(f"  {i}.  {user}")

    divider()
    step_ok(f"{n} profils sauvegardés dans data/users.json")
    pause()

    return load_users()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉTAPE 3 — VUE GLOBALE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def etape_3_vue_globale(users_data):
    clear()
    title("ÉTAPE 3 — VUE GLOBALE")

    import numpy as np

    all_steps = []
    all_calories = []
    all_scores = []

    loading_bar("  Calcul des statistiques globales", 1.0)
    print()

    scores_list = []
    for user_dict in users_data:
        user = User(
            name=user_dict["name"],
            age=user_dict["age"],
            goal=user_dict["goal"]
        )
        user.daily_logs = user_dict["daily_logs"]
        workout = Workout(user)
        score, msg = workout.calculate_fit_score()
        scores_list.append((user_dict["name"], score, msg, user_dict["goal"]))

        for log in user_dict["daily_logs"]:
            all_steps.append(log["steps"])
            all_calories.append(log["calories"])
        all_scores.append(score)

    divider()
    print("  📊  STATISTIQUES GLOBALES")
    divider()
    time.sleep(0.2)
    print(f"     👥  Utilisateurs total    : {len(users_data)}")
    time.sleep(0.2)
    print(f"     👟  Moyenne pas/jour      : {int(np.mean(all_steps)):,}")
    time.sleep(0.2)
    print(f"     🔥  Moyenne calories/jour : {int(np.mean(all_calories)):,}")
    time.sleep(0.2)
    print(f"     🤖  FitScore moyen        : {int(np.mean(all_scores))}/100")
    time.sleep(0.2)
    print(f"     🏆  Meilleur FitScore     : {max(all_scores)}/100")
    time.sleep(0.2)
    print(f"     📉  FitScore le plus bas  : {min(all_scores)}/100")
    divider()

    print()
    print("  🏆  CLASSEMENT GÉNÉRAL — FITSCORES")
    divider()

    scores_list.sort(key=lambda x: x[1], reverse=True)
    medals = ["🥇", "🥈", "🥉"]

    for i, (name, score, msg, goal) in enumerate(scores_list, 1):
        time.sleep(0.2)
        medal = medals[i-1] if i <= 3 else f"  {i}."
        filled = score // 10
        bar = "█" * filled + "░" * (10 - filled)
        print(f"  {medal}  {name[:22]:<22} {bar} {score}/100")
        print(f"        🎯 {goal:<15}  {msg}")
        print()

    divider()

    print()
    print("  🎯  RÉPARTITION DES OBJECTIFS")
    divider()

    goals = {}
    for u in users_data:
        g = u["goal"]
        goals[g] = goals.get(g, 0) + 1

    for goal, count in goals.items():
        time.sleep(0.15)
        bar = "▓" * count
        print(f"     {goal:<20} {bar} ({count})")

    divider()
    pause()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉTAPE 4 — CHOISIR UN UTILISATEUR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def etape_4_choisir_user(users_data):
    clear()
    title("ÉTAPE 4 — CHOISIR UN UTILISATEUR")

    print("  Sélectionnez un utilisateur :\n")

    for i, u in enumerate(users_data, 1):
        user = User(
            name=u["name"],
            age=u["age"],
            goal=u["goal"]
        )
        user.daily_logs = u["daily_logs"]
        workout = Workout(user)
        score, _ = workout.calculate_fit_score()
        filled = score // 10
        bar = "█" * filled + "░" * (10 - filled)
        time.sleep(0.15)
        print(
            f"  {i}.  {u['name'][:22]:<22} "
            f"{bar} {score}/100 · {u['goal']}"
        )

    print()
    divider()

    while True:
        try:
            choice = int(ask(f"Votre choix (1-{len(users_data)})"))
            if 1 <= choice <= len(users_data):
                return users_data[choice - 1]
            else:
                print(f"  ❌  Choisissez entre 1 et {len(users_data)}")
        except ValueError:
            print("  ❌  Entrez un nombre valide")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MENU UTILISATEUR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def menu_utilisateur(user_dict, users_data):
    user = User(
        name=user_dict["name"],
        age=user_dict["age"],
        goal=user_dict["goal"]
    )
    user.daily_logs = user_dict["daily_logs"]
    workout = Workout(user)
    score, msg = workout.calculate_fit_score()

    while True:
        clear()

        divider("═")
        print(f"  👤  {user_dict['name']}")
        print(f"      🎯 {user_dict['goal']}  ·  "
              f"📅 {user_dict['age']} ans  ·  "
              f"🤖 FitScore : {score}/100")
        print(f"      {msg}")
        divider("═")

        print("""
  ╔══════════════════════════════════════════╗
  ║        QUE VOULEZ-VOUS VOIR ?           ║
  ╠══════════════════════════════════════════╣
  ║                                          ║
  ║   1.  💪  Plan d'entraînement du jour   ║
  ║   2.  📊  Analyse statistique           ║
  ║   3.  📈  Générer les graphiques        ║
  ║   4.  📅  Rapport hebdomadaire          ║
  ║   5.  🏅  Mes badges                    ║
  ║   6.  👈  Choisir un autre utilisateur  ║
  ║   7.  🔄  Vue globale                   ║
  ║   8.  ❌  Quitter                       ║
  ║                                          ║
  ╚══════════════════════════════════════════╝
        """)

        choice = ask("Votre choix").strip()

        if choice == "1":
            clear()
            title(f"💪 PLAN D'ENTRAÎNEMENT — {user_dict['name']}")
            loading_bar("  Récupération météo Abidjan", 0.8)
            weather = get_weather()
            print()
            divider()
            print(f"  {weather['icon']}  Météo : {weather['description']} — {weather['temperature']}°C")
            print(f"  💡  {weather['recommendation']}")
            divider()
            workout.generate_plan(weather_condition=weather["condition"])
            pause()

        elif choice == "2":
            clear()
            title(f"📊 ANALYSE STATISTIQUE — {user_dict['name']}")
            steps = [
                ("📐", "ANOVA — calories par workout..."),
                ("📈", "Régression linéaire..."),
                ("⚖️ ", "T-test apparié..."),
                ("📅", "Analyse hebdomadaire..."),
            ]
            for icon, text in steps:
                print(f"  {icon}  {text}", flush=True)
                time.sleep(0.5)
            print()
            divider()
            full_statistical_analysis([user_dict])
            divider()
            step_ok("Analyse terminée !")
            pause()

        elif choice == "3":
            clear()
            title(f"📈 GRAPHIQUES — {user_dict['name']}")
            charts = [
                ("📈", "Progression pas & calories..."),
                ("🏋️ ", "Fréquence des workouts..."),
                ("📦", "Distribution calories..."),
                ("🎯", "Répartition des objectifs..."),
            ]
            for icon, text in charts:
                print(f"  {icon}  {text}", flush=True)
                time.sleep(0.3)
            print()
            loading_bar("  Génération Matplotlib/Seaborn", 1.5)
            generate_all_charts([user_dict])
            print()
            divider()
            step_ok("Graphiques sauvegardés dans visualization/")
            divider()
            pause()

        elif choice == "4":
            clear()
            title(f"📅 RAPPORT HEBDOMADAIRE — {user_dict['name']}")
            loading_bar("  Génération du rapport", 0.8)
            print()
            generate_weekly_report(user_dict)
            pause()

        elif choice == "5":
            clear()
            title(f"🏅 BADGES — {user_dict['name']}")
            loading_bar("  Analyse des performances", 0.8)
            print()
            earned, not_earned = check_badges(user_dict, score)
            print()
            divider()
            print(f"  📊  Score badges : {len(earned)}/{len(ALL_BADGES)}")
            filled = int((len(earned) / len(ALL_BADGES)) * 20)
            bar = "█" * filled + "░" * (20 - filled)
            print(f"  [{bar}] {int(len(earned)/len(ALL_BADGES)*100)}%")
            divider()
            pause()

        elif choice == "6":
            user_dict = etape_4_choisir_user(users_data)
            user = User(
                name=user_dict["name"],
                age=user_dict["age"],
                goal=user_dict["goal"]
            )
            user.daily_logs = user_dict["daily_logs"]
            workout = Workout(user)
            score, msg = workout.calculate_fit_score()

        elif choice == "7":
            etape_3_vue_globale(users_data)

        elif choice == "8":
            goodbye()
            sys.exit(0)

        else:
            print("  ❌  Option invalide")
            time.sleep(1)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ÉCRAN FIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def goodbye():
    clear()
    print()
    time.sleep(0.3)
    divider("═")
    print("  ║" + " " * 18 + "👋 FitSync AI" + " " * 19 + "║")
    divider("═")
    print()
    type_text("  À bientôt sur FitSync AI 🏋️", delay=0.05)
    type_text("  FitSync Masters — Rabiatou & Dia Oumar 💪", delay=0.04)
    type_text("  COT_GenAI 2026 🎓", delay=0.04)
    print()
    time.sleep(0.5)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    splash_screen()
    etape_1_pipeline()
    users_data = etape_2_profils()
    etape_3_vue_globale(users_data)
    user_dict = etape_4_choisir_user(users_data)
    menu_utilisateur(user_dict, users_data)


if __name__ == "__main__":
    main()