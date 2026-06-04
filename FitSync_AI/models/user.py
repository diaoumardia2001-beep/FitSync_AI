from faker import Faker
import random
from datetime import datetime, timedelta

faker = Faker()

GOALS = ["weight_loss", "strength", "cardio", "flexibility"]
WORKOUTS = ["Yoga", "Running", "HIIT", "Strength Training", "Cycling", "Walking"]

class User:
    def __init__(self, name=None, age=None, goal=None):
        self.name = name or faker.name()
        self.age = age or random.randint(18, 60)
        self.goal = goal or random.choice(GOALS)
        self.daily_logs = []

    def add_log(self, date, steps, calories, workout):
        log = {
            "date": date,
            "steps": steps,
            "calories": calories,
            "workout": workout
        }
        self.daily_logs.append(log)

    def generate_fake_logs(self, days=30):
        for i in range(days):
            date = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
            self.add_log(
                date=date,
                steps=random.randint(2000, 15000),
                calories=random.randint(200, 800),
                workout=random.choice(WORKOUTS)
            )

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "goal": self.goal,
            "daily_logs": self.daily_logs
        }

    def __str__(self):
        return f"User: {self.name} | Age: {self.age} | Goal: {self.goal} | Logs: {len(self.daily_logs)} days"


def generate_fake_users(n=5):
    users = []
    for _ in range(n):
        user = User()
        user.generate_fake_logs(days=30)
        users.append(user)
    return users