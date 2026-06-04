import json
import os

DATA_FILE = "data/users.json"

def save_users(users):
    """Sauvegarde la liste des utilisateurs dans le fichier JSON"""
    data = [user.to_dict() for user in users]
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ {len(users)} utilisateurs sauvegardés dans {DATA_FILE}")


def load_users():
    """Charge les utilisateurs depuis le fichier JSON"""
    if not os.path.exists(DATA_FILE):
        print("⚠️ Aucun fichier de données trouvé.")
        return []
    
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    
    print(f"✅ {len(data)} utilisateurs chargés.")
    return data