WORKOUT_RECOMMENDATIONS = {
    "weight_loss": {
        "faible": "🚶 Commencez par 20 min de marche rapide + 10 min de Yoga",
        "moyen":  "🔥 Essayez 30 min de HIIT pour brûler plus de calories",
        "élevé":  "🏃 Excellent niveau ! 45 min de Running + abdos"
    },
    "strength": {
        "faible": "💪 Commencez par 20 min de musculation légère",
        "moyen":  "🏋️ Faites 40 min de Strength Training ciblé",
        "élevé":  "🏋️ Super ! 60 min de Strength Training intensif"
    },
    "cardio": {
        "faible": "🚴 Commencez par 20 min de Cycling léger",
        "moyen":  "🏃 Faites 30 min de Running à rythme modéré",
        "élevé":  "⚡ 45 min de Running + 15 min de HIIT"
    },
    "flexibility": {
        "faible": "🧘 20 min de Yoga doux pour commencer",
        "moyen":  "🧘 40 min de Yoga + étirements",
        "élevé":  "🌟 60 min de Yoga avancé + méditation"
    }
}


class Workout:
    """
    Classe principale de génération de plans d'entraînement
    Analyse l'activité passée et génère des recommandations
    """
    def __init__(self, user):
        self.user = user

    def get_activity_level(self):
        """
        Détermine le niveau d'activité selon
        la moyenne des pas des 7 derniers jours
        """
        avg_steps = self.user.get_average_steps()
        if avg_steps < 5000:
            return "faible"
        elif avg_steps < 10000:
            return "moyen"
        else:
            return "élevé"

    def calculate_fit_score(self):
        """
        Calcule un score de forme sur 100 basé sur :
        - Moyenne des pas       → 40 points max
        - Moyenne des calories  → 30 points max
        - Régularité            → 30 points max
        """
        if not self.user.daily_logs:
            return 0, "⚠️ Aucune donnée disponible"

        logs = self.user.daily_logs

        # 1. Score des pas (40 pts max)
        avg_steps = sum(
            l["steps"] for l in logs
        ) / len(logs)
        steps_score = min(40, (avg_steps / 15000) * 40)

        # 2. Score des calories (30 pts max)
        avg_calories = sum(
            l["calories"] for l in logs
        ) / len(logs)
        calories_score = min(30, (avg_calories / 800) * 30)

        # 3. Score de régularité (30 pts max)
        active_days = sum(
            1 for l in logs if l["steps"] > 5000
        )
        regularity_score = min(
            30, (active_days / len(logs)) * 30
        )

        total = int(
            steps_score + calories_score + regularity_score
        )

        # Message selon le score
        if total >= 80:
            message = "🏆 Excellent niveau ! Continuez comme ça !"
        elif total >= 60:
            message = "💪 Bon niveau, vous progressez bien !"
        elif total >= 40:
            message = "📈 Niveau moyen, soyez plus régulier"
        else:
            message = "⚠️ Activité faible, commencez doucement"

        return total, message

    def generate_plan(self, weather_condition=None):
        """
        Génère un plan d'entraînement personnalisé
        Prend en compte la météo si disponible
        """
        avg_steps = self.user.get_average_steps()
        avg_calories = self.user.get_average_calories()
        goal = self.user.goal
        level = self.get_activity_level()
        score, score_msg = self.calculate_fit_score()

        # Recommandation de base
        recommendation = WORKOUT_RECOMMENDATIONS.get(
            goal, WORKOUT_RECOMMENDATIONS["cardio"]
        )[level]

        # Adaptation météo
        if weather_condition:
            if weather_condition == "rain":
                recommendation += (
                    "\n🌧️ Pluie détectée → "
                    "Entraînement en intérieur recommandé"
                )
            elif weather_condition == "hot":
                recommendation += (
                    "\n☀️ Forte chaleur → "
                    "Hydratez-vous bien, réduisez l'intensité"
                )
            elif weather_condition == "clear":
                recommendation += (
                    "\n🌤️ Beau temps → "
                    "Profitez de l'extérieur !"
                )

        print(f"\n{'='*50}")
        print(f"👤 Utilisateur  : {self.user.name}")
        print(f"🎯 Objectif     : {goal}")
        print(f"👟 Moy. pas     : {avg_steps:.0f} pas/jour")
        print(f"🔥 Moy. calories: {avg_calories:.0f} cal/jour")
        print(f"📊 Niveau       : {level}")
        print(f"🤖 FitScore     : {score}/100 — {score_msg}")
        print(f"💪 Plan du jour : {recommendation}")
        print(f"{'='*50}")

        return {
            "name": self.user.name,
            "goal": goal,
            "level": level,
            "avg_steps": round(avg_steps),
            "avg_calories": round(avg_calories),
            "fit_score": score,
            "score_message": score_msg,
            "recommendation": recommendation
        }

    def get_weekly_summary(self):
        """
        Résumé des 7 derniers jours d'activité
        Utilise map et filter (cours)
        """
        if not self.user.daily_logs:
            return {}

        last_7 = self.user.daily_logs[:7]

        # Utilisation de MAP (cours)
        all_steps = list(map(
            lambda l: l["steps"], last_7
        ))
        all_calories = list(map(
            lambda l: l["calories"], last_7
        ))
        all_workouts = list(map(
            lambda l: l["workout"], last_7
        ))

        # Utilisation de FILTER (cours)
        active_days = list(filter(
            lambda l: l["steps"] > 5000, last_7
        ))

        return {
            "total_steps": sum(all_steps),
            "total_calories": sum(all_calories),
            "active_days": len(active_days),
            "favorite_workout": max(
                set(all_workouts),
                key=all_workouts.count
            ),
            "best_day": max(
                last_7, key=lambda l: l["steps"]
            ),
            "worst_day": min(
                last_7, key=lambda l: l["steps"]
            )
        }