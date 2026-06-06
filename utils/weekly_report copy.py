from datetime import datetime, timedelta
from functools import reduce


def generate_weekly_report(user_dict):
    """
    Génère un rapport hebdomadaire complet
    pour un utilisateur
    Accepte un dictionnaire (chargé depuis JSON)
    """
    name = user_dict.get("name", "Inconnu")
    logs = user_dict.get("daily_logs", [])

    if not logs:
        print("⚠️ Aucun log disponible")
        return {}

    # Prendre les 7 derniers jours
    last_7 = logs[:7]

    # Utilisation de MAP (cours)
    all_steps = list(map(
        lambda l: l.get("steps", 0), last_7
    ))
    all_calories = list(map(
        lambda l: l.get("calories", 0), last_7
    ))
    all_workouts = list(map(
        lambda l: l.get("workout", "Unknown"), last_7
    ))
    all_dates = list(map(
        lambda l: l.get("date", ""), last_7
    ))

    # Utilisation de REDUCE (cours)
    total_steps = reduce(lambda x, y: x + y, all_steps)
    total_calories = reduce(
        lambda x, y: x + y, all_calories
    )

    # Utilisation de FILTER (cours)
    active_days = list(filter(
        lambda s: s > 5000, all_steps
    ))

    # Calculs
    avg_steps = total_steps // len(last_7)
    avg_calories = total_calories // len(last_7)
    best_day_idx = all_steps.index(max(all_steps))
    worst_day_idx = all_steps.index(min(all_steps))
    favorite_workout = max(
        set(all_workouts),
        key=all_workouts.count
    )

    # Comparaison semaine précédente
    prev_7 = logs[7:14] if len(logs) >= 14 else []
    if prev_7:
        prev_steps = list(map(
            lambda l: l.get("steps", 0), prev_7
        ))
        prev_total = reduce(lambda x, y: x + y, prev_steps)
        evolution = total_steps - prev_total
        evolution_pct = round(
            (evolution / prev_total) * 100, 1
        ) if prev_total > 0 else 0
    else:
        evolution = 0
        evolution_pct = 0

    report = {
        "name": name,
        "period_start": all_dates[-1] if all_dates else "",
        "period_end": all_dates[0] if all_dates else "",
        "total_steps": total_steps,
        "total_calories": total_calories,
        "avg_steps": avg_steps,
        "avg_calories": avg_calories,
        "active_days": len(active_days),
        "sessions": len(last_7),
        "favorite_workout": favorite_workout,
        "best_day": {
            "date": all_dates[best_day_idx],
            "steps": all_steps[best_day_idx]
        },
        "worst_day": {
            "date": all_dates[worst_day_idx],
            "steps": all_steps[worst_day_idx]
        },
        "evolution_steps": evolution,
        "evolution_pct": evolution_pct
    }

    display_weekly_report(report)
    return report


def display_weekly_report(report):
    """
    Affiche le rapport hebdomadaire formaté
    """
    evolution_icon = (
        "📈" if report["evolution_steps"] >= 0 else "📉"
    )
    evolution_sign = (
        "+" if report["evolution_steps"] >= 0 else ""
    )

    print(f"\n{'┌' + '─'*43 + '┐'}")
    print(
        f"│{'📊 RAPPORT SEMAINE — ' + report['name']:^43}│"
    )
    print(f"{'├' + '─'*43 + '┤'}")
    print(
        f"│ 📅 Période  : "
        f"{report['period_start']} → "
        f"{report['period_end']:<20}│"
    )
    print(
        f"│ 👟 Total pas      : "
        f"{report['total_steps']:>8,} pas          │"
    )
    print(
        f"│ 🔥 Total calories : "
        f"{report['total_calories']:>8,} cal          │"
    )
    print(
        f"│ 🏋️  Séances        : "
        f"{report['sessions']:>8} séances       │"
    )
    print(
        f"│ ✅ Jours actifs   : "
        f"{report['active_days']:>8} jours         │"
    )
    print(
        f"│ 💪 Workout favori : "
        f"{report['favorite_workout']:<22}│"
    )
    print(f"{'├' + '─'*43 + '┤'}")
    print(
        f"│ 🏆 Meilleur jour  : "
        f"{report['best_day']['date']} "
        f"({report['best_day']['steps']:,} pas) │"
    )
    print(
        f"│ 📉 Jour faible    : "
        f"{report['worst_day']['date']} "
        f"({report['worst_day']['steps']:,} pas) │"
    )
    print(f"{'├' + '─'*43 + '┤'}")
    print(
        f"│ {evolution_icon} Évolution      : "
        f"{evolution_sign}"
        f"{report['evolution_steps']:,} pas "
        f"({evolution_sign}"
        f"{report['evolution_pct']}%)          │"
    )
    print(f"{'└' + '─'*43 + '┘'}")