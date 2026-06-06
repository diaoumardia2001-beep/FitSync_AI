import json
import os
import csv
from datetime import datetime

# Chemins des fichiers
USERS_FILE = "data/users.json"
RAW_FILE = "data/raw_data.json"
CLEAN_FILE = "data/clean_data.json"
PROCESSED_FILE = "data/preprocessed_data.json"


def save_users(users):
    """
    Sauvegarde la liste des utilisateurs en JSON
    Encapsulation : convertit les objets User en dict
    """
    os.makedirs("data", exist_ok=True)
    data = [user.to_dict() for user in users]

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ {len(users)} utilisateurs sauvegardés")
    return True


def load_users():
    """
    Charge les utilisateurs depuis le fichier JSON
    Retourne une liste de dictionnaires
    """
    if not os.path.exists(USERS_FILE):
        print("⚠️ Aucun fichier utilisateurs trouvé")
        return []

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✅ {len(data)} utilisateurs chargés")
    return data


def save_json(data, filepath):
    """
    Sauvegarde générique en JSON
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Données sauvegardées : {filepath}")
    return True


def load_json(filepath):
    """
    Chargement générique depuis JSON
    """
    if not os.path.exists(filepath):
        print(f"⚠️ Fichier introuvable : {filepath}")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def save_csv(data, filepath):
    """
    Sauvegarde des données en CSV
    """
    if not data:
        print("⚠️ Aucune donnée à sauvegarder")
        return False

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="",
              encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ CSV sauvegardé : {filepath}")
    return True


def load_csv(filepath):
    """
    Chargement depuis un fichier CSV
    """
    if not os.path.exists(filepath):
        print(f"⚠️ Fichier introuvable : {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    print(f"✅ {len(data)} lignes chargées depuis {filepath}")
    return data


def export_report(content, filename=None):
    """
    Exporte un rapport texte dans reports/
    """
    os.makedirs("reports", exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/report_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Rapport exporté : {filename}")
    return filename


def file_exists(filepath):
    """Vérifie si un fichier existe"""
    return os.path.exists(filepath)


def get_file_info(filepath):
    """
    Retourne les infos d'un fichier
    """
    if not os.path.exists(filepath):
        return None

    stat = os.stat(filepath)
    return {
        "path": filepath,
        "size_kb": round(stat.st_size / 1024, 2),
        "modified": datetime.fromtimestamp(
            stat.st_mtime
        ).strftime("%Y-%m-%d %H:%M:%S")
    }