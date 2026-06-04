class Workout:
    def __init__(self, user):
        self.user = user

    def get_average_steps(self):
        """Calcule la moyenne des pas des 7 derniers jours"""
        if not self.user.daily_logs:
            return 0
        last_7 = self.user.daily_logs[:7]
        total_steps = sum(log["steps"] for log in last_7)
        return total_steps / len(last_7)

    def get_average_calories(self):
        """Calcule la moyenne des calories des 7 derniers jours"""
        if not self.user.daily_logs:
            return 0
        last_7 = self.user.daily_logs[:7]
        total_calories = sum(log["calories"] for log in last_7)
        return total_calories / len(last_7)

    def generate_plan(self):
        """Génère un plan d'entraînement personnalisé"""
        avg_steps = self.get_average_steps()
        avg_calories = self.get_average_calories()
        goal = self.user.goal

        print(f"\n👤 Utilisateur : {self.user.name}")
        print(f"🎯 Objectif    : {goal}")
        print(f"👟 Moyenne pas : {avg_steps:.0f} pas/jour")
        print(f"🔥 Moyenne cal : {avg_calories:.0f} cal/jour")
        print(f"💪 Recommandation : {self._recommend(goal, avg_steps)}")

    def _recommend(self, goal, avg_steps):
        """Logique de recommandation selon objectif et activité"""

        # Activité faible → entraînement léger
        if avg_steps < 5000:
            niveau = "faible"
        elif avg_steps < 10000:
            niveau = "moyen"
        else:
            niveau = "élevé"

        recommendations = {
            "weight_loss": {
                "faible": "Commencez par 20 min de marche rapide + 10 min de Yoga 🧘",
                "moyen": "Essayez 30 min de HIIT pour brûler plus de calories 🔥",
                "élevé": "Excellent niveau ! Faites 45 min de Running + abdos 🏃"
            },
            "strength": {
                "faible": "Commencez par 20 min de musculation légère 💪",
                "moyen": "Faites 40 min de Strength Training ciblé 🏋️",
                "élevé": "Super ! 60 min de Strength Training intensif 🏋️‍♀️"
            },
            "cardio": {
                "faible": "Commencez par 20 min de Cycling léger 🚴",
                "moyen": "Faites 30 min de Running à rythme modéré 🏃",
                "élevé": "45 min de Running + 15 min de HIIT 🔥"
            },
            "flexibility": {
                "faible": "20 min de Yoga doux pour commencer 🧘",
                "moyen": "40 min de Yoga + étirements 🧘‍♀️",
                "élevé": "60 min de Yoga avancé + méditation 🌟"
            }
        }

        return recommendations[goal][niveau]