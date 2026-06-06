import json # Bibliothèque native pour manipuler le format JSON (très utilisé pour échanger des données)
import os   # Bibliothèque pour vérifier si des fichiers existent sur l'ordinateur

DATA_FILE = "data/users.json" # Chemin vers notre base de données "légère"

def save_users(users):
    """
    Transforme nos objets Python en format JSON pour les enregistrer sur le disque.
    """
    # Liste de compréhension : on transforme chaque objet User en dictionnaire via .to_dict()
    data = [user.to_dict() for user in users]
    
    # On ouvre le fichier en mode écriture ('w')
    with open(DATA_FILE, "w") as f:
        # json.dump convertit la liste de dictionnaires en un fichier texte lisible
        json.dump(data, f, indent=4) # indent=4 rend le fichier "joli" et humainement lisible
        
    print(f"✅ {len(users)} utilisateurs sauvegardés dans {DATA_FILE}")


def load_users():
    """
    Lit le fichier JSON et récupère les données.
    """
    # Sécurité : on vérifie si le fichier existe avant d'essayer de l'ouvrir
    if not os.path.exists(DATA_FILE):
        print("⚠️ Aucun fichier de données trouvé.")
        return []
    
    # On ouvre le fichier en mode lecture ('r')
    with open(DATA_FILE, "r") as f:
        # json.load transforme le texte du fichier en objets Python (listes et dictionnaires)
        data = json.load(f)
    
    print(f"✅ {len(data)} utilisateurs chargés.")
    return data