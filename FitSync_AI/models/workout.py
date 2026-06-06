class Workout:
    """
    La classe Workout est un 'moteur de recommandation'.
    """
    
    # Définition du dictionnaire à l'intérieur ou à l'extérieur de la classe
    RECOMMENDATIONS = {
        "weight_loss": {
            "faible": "Commencez par 20 min de marche rapide + 10 min de Yoga 🧘",
            "moyen": "Essayez 30 min de HIIT pour brûler plus de calories 🔥",
            "élevé": "Excellent niveau ! Faites 45 min de Running + abdos 🏃"
        },
        "muscle_gain": {
            "faible": "Pompes sur les genoux et squats simples 💪",
            "moyen": "Musculation haut du corps (haltères) 🏋️",
            "élevé": "Entraînement intensif : Full body avec charges 🏗️"
        },
        "strength": {
            "faible": "Squats au poids du corps et fentes ⚡",
            "moyen": "Musculation : soulevé de terre et développé couché 🏋️",
            "élevé": "Haltérophilie et renforcement intensif 💥"
        },
        "cardio": {
            "faible": "20 min de marche lente 🚶",
            "moyen": "30 min de jogging à rythme régulier 🏃",
            "élevé": "45 min de course rapide ou fractionné ⚡"
        }
    }

    def __init__(self, user):
        self.user = user

    def get_average_steps(self):
        if not self.user.daily_logs: return 0
        last_7 = self.user.daily_logs[:7]
        return sum(log["steps"] for log in last_7) / len(last_7)

    def generate_plan(self):
        avg_steps = self.get_average_steps()
        goal = self.user.goal
        
        # Détermination du niveau
        if avg_steps < 5000: niveau = "faible"
        elif avg_steps < 10000: niveau = "moyen"
        else: niveau = "élevé"

        # Logique sécurisée pour éviter KeyError
        # On cherche l'objectif, si inconnu on prend 'cardio', puis on cherche le niveau
        goal_data = self.RECOMMENDATIONS.get(goal, self.RECOMMENDATIONS["cardio"])
        recommendation = goal_data.get(niveau, goal_data["faible"])

        print(f"\n👤 Utilisateur : {self.user.name}")
        print(f"🎯 Objectif    : {goal}")
        print(f"💪 Recommandation : {recommendation}")