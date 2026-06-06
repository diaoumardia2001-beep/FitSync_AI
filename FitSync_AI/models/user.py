from faker import Faker # Bibliothèque pour générer de fausses données réalistes
import random           # Module pour introduire de l'aléatoire dans les données
from datetime import datetime, timedelta # Pour gérer les dates de façon dynamique

faker = Faker() # Création de l'instance qui va générer les noms, etc.

# Constantes définissant les choix possibles pour les utilisateurs
GOALS = ["weight_loss", "strength", "cardio", "flexibility"]
WORKOUTS = ["Yoga", "Running", "HIIT", "Strength Training", "Cycling", "Walking"]

class User:
    """
    La classe User représente un utilisateur de l'application.
    Elle encapsule toutes ses informations et ses activités.
    """
    def __init__(self, name=None, age=None, goal=None):
        # Si aucun nom/âge/objectif n'est fourni, on utilise Faker ou Random pour en créer un par défaut
        self.name = name or faker.name()
        self.age = age or random.randint(18, 60)
        self.goal = goal or random.choice(GOALS)
        self.daily_logs = [] # Liste vide qui contiendra tous les enregistrements quotidiens

    def add_log(self, date, steps, calories, workout):
        """Méthode pour ajouter une activité dans l'historique de l'utilisateur."""
        log = {
            "date": date,
            "steps": steps,
            "calories": calories,
            "workout": workout
        }
        self.daily_logs.append(log) # Ajoute le dictionnaire log à la liste des logs

    def generate_fake_logs(self, days=30):
        """Génère automatiquement 30 jours de données fictives pour simuler un historique."""
        for i in range(days):
            # Calcule la date correspondant au jour actuel moins 'i' jours
            date = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
            self.add_log(
                date=date,
                steps=random.randint(2000, 15000),   # Pas aléatoires entre 2k et 15k
                calories=random.randint(200, 800),   # Calories aléatoires
                workout=random.choice(WORKOUTS)      # Un sport choisi au hasard
            )

    def to_dict(self):
        """Convertit l'objet utilisateur en dictionnaire (pratique pour le JSON/Pandas)."""
        return {
            "name": self.name,
            "age": self.age,
            "goal": self.goal,
            "daily_logs": self.daily_logs
        }

    def __str__(self):
        """Méthode spéciale pour afficher une description lisible de l'utilisateur."""
        return f"User: {self.name} | Age: {self.age} | Goal: {self.goal} | Logs: {len(self.daily_logs)} days"


def generate_fake_users(n=5):
    """Fonction utilitaire pour créer une liste de 'n' utilisateurs générés aléatoirement."""
    users = []
    for _ in range(n):
        user = User() # Création d'un nouvel objet utilisateur
        user.generate_fake_logs(days=30) # On génère son historique
        users.append(user) # On l'ajoute à la liste des utilisateurs
    return users