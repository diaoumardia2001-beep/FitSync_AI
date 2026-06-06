from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

GOALS = ["weight_loss", "strength", "cardio", "flexibility"]
WORKOUTS = ["Yoga", "Running", "HIIT", 
            "Strength Training", "Cycling", "Walking"]


class User:
    """
    Classe représentant un utilisateur du tracker fitness
    Encapsule les données personnelles et les logs d'activité
    """
    def __init__(self, name=None, age=None, goal=None):
        self.name = name or fake.name()
        self.age = age or random.randint(18, 60)
        self.goal = goal or random.choice(GOALS)
        self.daily_logs = []

    def add_log(self, date, steps, calories, workout):
        """Ajoute un log d'activité quotidien"""
        log = {
            "date": date,
            "steps": steps,
            "calories": calories,
            "workout": workout
        }
        self.daily_logs.append(log)

    def generate_fake_logs(self, days=30):
        """Génère des logs fictifs sur N jours"""
        for i in range(days):
            date = (
                datetime.today() - timedelta(days=i)
            ).strftime("%Y-%m-%d")
            self.add_log(
                date=date,
                steps=random.randint(2000, 15000),
                calories=random.randint(200, 800),
                workout=random.choice(WORKOUTS)
            )

    def get_average_steps(self):
        """Calcule la moyenne des pas sur 7 derniers jours"""
        if not self.daily_logs:
            return 0
        last_7 = self.daily_logs[:7]
        return sum(log["steps"] for log in last_7) / len(last_7)

    def get_average_calories(self):
        """Calcule la moyenne des calories sur 7 derniers jours"""
        if not self.daily_logs:
            return 0
        last_7 = self.daily_logs[:7]
        return sum(
            log["calories"] for log in last_7
        ) / len(last_7)

    def to_dict(self):
        """Sérialise l'utilisateur en dictionnaire"""
        return {
            "name": self.name,
            "age": self.age,
            "goal": self.goal,
            "daily_logs": self.daily_logs
        }

    def __str__(self):
        return (
            f"User: {self.name} | "
            f"Age: {self.age} | "
            f"Goal: {self.goal} | "
            f"Logs: {len(self.daily_logs)} jours"
        )

    def __repr__(self):
        return f"User(name={self.name}, goal={self.goal})"


class ActiveUser(User):
    """
    Héritage : utilisateur très actif
    Génère des logs avec plus de steps et calories
    """
    def __init__(self, name=None, age=None, goal=None):
        super().__init__(name, age, goal)
        self.user_type = "active"

    def generate_fake_logs(self, days=30):
        """Override : logs avec activité élevée"""
        for i in range(days):
            date = (
                datetime.today() - timedelta(days=i)
            ).strftime("%Y-%m-%d")
            self.add_log(
                date=date,
                steps=random.randint(10000, 20000),
                calories=random.randint(500, 1000),
                workout=random.choice(WORKOUTS)
            )


class BeginnerUser(User):
    """
    Héritage : utilisateur débutant
    Génère des logs avec moins de steps et calories
    """
    def __init__(self, name=None, age=None, goal=None):
        super().__init__(name, age, goal)
        self.user_type = "beginner"

    def generate_fake_logs(self, days=30):
        """Override : logs avec activité faible"""
        for i in range(days):
            date = (
                datetime.today() - timedelta(days=i)
            ).strftime("%Y-%m-%d")
            self.add_log(
                date=date,
                steps=random.randint(1000, 5000),
                calories=random.randint(100, 300),
                workout=random.choice(WORKOUTS)
            )


def generate_fake_users(n=5):
    """
    Génère N utilisateurs fictifs avec Faker
    Mix de profils : normal, actif, débutant
    """
    users = []
    user_types = [User, ActiveUser, BeginnerUser]

    for _ in range(n):
        UserClass = random.choice(user_types)
        user = UserClass()
        user.generate_fake_logs(days=30)
        users.append(user)

    return users