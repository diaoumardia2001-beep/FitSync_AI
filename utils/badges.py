from functools import reduce

# Définition de tous les badges disponibles
ALL_BADGES = {
    "marathon_walker": {
        "icon": "🥇",
        "name": "Marathon Walker",
        "desc": "10 000 pas/jour pendant 7 jours consécutifs",
        "color": "gold"
    },
    "calorie_crusher": {
        "icon": "🔥",
        "name": "Calorie Crusher",
        "desc": "600+ calories brûlées en une journée",
        "color": "red"
    },
    "consistency_king": {
        "icon": "👑",
        "name": "Consistency King",
        "desc": "30 jours actifs consécutifs (> 5000 pas)",
        "color": "purple"
    },
    "yoga_master": {
        "icon": "🧘",
        "name": "Yoga Master",
        "desc": "Yoga pratiqué 10 fois ou plus",
        "color": "green"
    },
    "speed_runner": {
        "icon": "🏃",
        "name": "Speed Runner",
        "desc": "Running pratiqué 10 fois ou plus",
        "color": "blue"
    },
    "hiit_champion": {
        "icon": "⚡",
        "name": "HIIT Champion",
        "desc": "HIIT pratiqué 10 fois ou plus",
        "color": "orange"
    },
    "all_rounder": {
        "icon": "🌟",
        "name": "All Rounder",
        "desc": "Tous les types de workout pratiqués",
        "color": "cyan"
    },
    "goal_crusher": {
        "icon": "🎯",
        "name": "Goal Crusher",
        "desc": "FitScore supérieur à 80/100",
        "color": "green"
    },
    "early_bird": {
        "icon": "🌅",
        "name": "Early Bird",
        "desc": "Plus de 20 jours actifs sur 30",
        "color": "yellow"
    },
    "iron_will": {
        "icon": "🦾",
        "name": "Iron Will",
        "desc": "Moyenne de pas > 10 000 sur 30 jours",
        "color": "gray"
    }
}

ALL_WORKOUTS = {
    "Yoga", "Running", "HIIT",
    "Strength Training", "Cycling", "Walking"
}


def check_badges(user_dict, fit_score=0):
    """
    Vérifie et attribue les badges
    selon les performances de l'utilisateur
    Retourne les badges obtenus et non obtenus
    """
    logs = user_dict.get("daily_logs", [])
    earned = []
    not_earned = []

    if not logs:
        return [], list(ALL_BADGES.keys())

    # Extraction des données avec MAP
    all_steps = list(map(
        lambda l: l.get("steps", 0), logs
    ))
    all_calories = list(map(
        lambda l: l.get("calories", 0), logs
    ))
    all_workouts = list(map(
        lambda l: l.get("workout", ""), logs
    ))

    # FILTER : jours actifs
    active_days = list(filter(
        lambda s: s > 5000, all_steps
    ))

    # REDUCE : total calories
    total_calories = reduce(
        lambda x, y: x + y, all_calories
    ) if all_calories else 0

    # Moyenne des pas
    avg_steps = sum(all_steps) / len(all_steps) \
        if all_steps else 0

    # ── Vérification de chaque badge ──

    # 1. Marathon Walker
    # 7 jours consécutifs > 10 000 pas
    consecutive = 0
    max_consecutive = 0
    for s in all_steps:
        if s >= 10000:
            consecutive += 1
            max_consecutive = max(
                max_consecutive, consecutive
            )
        else:
            consecutive = 0

    if max_consecutive >= 7:
        earned.append("marathon_walker")
    else:
        not_earned.append("marathon_walker")

    # 2. Calorie Crusher
    max_calories = max(all_calories) if all_calories else 0
    if max_calories >= 600:
        earned.append("calorie_crusher")
    else:
        not_earned.append("calorie_crusher")

    # 3. Consistency King
    if len(active_days) >= 30:
        earned.append("consistency_king")
    else:
        not_earned.append("consistency_king")

    # 4. Yoga Master
    yoga_count = all_workouts.count("Yoga")
    if yoga_count >= 10:
        earned.append("yoga_master")
    else:
        not_earned.append("yoga_master")

    # 5. Speed Runner
    running_count = all_workouts.count("Running")
    if running_count >= 10:
        earned.append("speed_runner")
    else:
        not_earned.append("speed_runner")

    # 6. HIIT Champion
    hiit_count = all_workouts.count("HIIT")
    if hiit_count >= 10:
        earned.append("hiit_champion")
    else:
        not_earned.append("hiit_champion")

    # 7. All Rounder
    unique_workouts = set(all_workouts)
    if ALL_WORKOUTS.issubset(unique_workouts):
        earned.append("all_rounder")
    else:
        not_earned.append("all_rounder")

    # 8. Goal Crusher
    if fit_score >= 80:
        earned.append("goal_crusher")
    else:
        not_earned.append("goal_crusher")

    # 9. Early Bird
    if len(active_days) >= 20:
        earned.append("early_bird")
    else:
        not_earned.append("early_bird")

    # 10. Iron Will
    if avg_steps >= 10000:
        earned.append("iron_will")
    else:
        not_earned.append("iron_will")

    display_badges(
        user_dict.get("name", "Inconnu"),
        earned,
        not_earned
    )

    return earned, not_earned


def display_badges(name, earned, not_earned):
    """
    Affiche les badges obtenus et non obtenus
    """
    print(f"\n{'='*50}")
    print(f"🏅 BADGES — {name}")
    print(f"{'='*50}")

    if earned:
        print(f"\n✅ Badges obtenus ({len(earned)}) :")
        for badge_key in earned:
            badge = ALL_BADGES[badge_key]
            print(
                f"  {badge['icon']} {badge['name']}"
                f" → {badge['desc']}"
            )
    else:
        print("\n❌ Aucun badge obtenu pour l'instant")

    if not_earned:
        print(f"\n🔒 Badges à débloquer ({len(not_earned)}) :")
        for badge_key in not_earned:
            badge = ALL_BADGES[badge_key]
            print(
                f"  ⬜ {badge['name']}"
                f" → {badge['desc']}"
            )

    print(f"\n📊 Score badges : "
          f"{len(earned)}/{len(ALL_BADGES)}")
    print(f"{'='*50}")


def get_badge_progress(user_dict):
    """
    Retourne le pourcentage de badges obtenus
    """
    earned, _ = check_badges(user_dict)
    return round(len(earned) / len(ALL_BADGES) * 100, 1)