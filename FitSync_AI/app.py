import streamlit as st           # Framework pour créer l'interface web rapidement
import pandas as pd              # Bibliothèque pour la manipulation et l'analyse de données
import matplotlib.pyplot as plt  # Bibliothèque pour générer des graphiques statiques
import seaborn as sns            # Bibliothèque pour des graphiques statistiques plus esthétiques

# Importation de vos fonctions métiers personnalisées
from models.user import generate_fake_users
from utils.file_manager import save_users, load_users

# Tentative d'importation de la météo, avec une fonction de repli (fallback) si le module échoue
try:
    from utils.weather import get_weather
except:
    def get_weather():
        return {"city": "Abidjan", "temperature": 28, "description": "Ciel dégagé", "icon": "☀️", "recommendation": "Conditions idéales pour l'entraînement !"}

# Configuration globale de l'interface (titre dans l'onglet, mode large)
st.set_page_config(page_title="FitSync AI", page_icon="🏋️", layout="wide")

# Affichage du titre et sous-titre de l'application
st.title("🏋️ FitSync AI")
st.subheader("Coach Fitness Intelligent - Hackathon 2026")

# Création du menu de navigation dans la barre latérale
page = st.sidebar.radio("Navigation", [
    "🏠 Accueil", 
    "💪 Profil Utilisateur", 
    "📊 Statistiques Globales", 
    "📈 Visualisations"
])

# Chargement initial des données utilisateurs depuis le fichier JSON/local
users_data = load_users()

# ===================== ACCUEIL =====================
if page == "🏠 Accueil":
    # Bouton pour générer de nouvelles données de test
    if st.button("🔄 Générer 5 nouveaux profils"):
        with st.spinner("Génération..."):
            save_users(generate_fake_users(5)) # Appel à la fonction de création
        st.success("✅ 5 profils générés !")
        st.rerun() # Recharge la page pour mettre à jour l'affichage
    
    # Message de confirmation si des données sont présentes
    if users_data:
        st.success(f"{len(users_data)} utilisateurs chargés dans la base.")

# ===================== PROFIL UTILISATEUR =====================
elif page == "💪 Profil Utilisateur":
    if not users_data:
        st.warning("Génère d'abord des profils sur Accueil")
    else:
        # Sélecteur pour choisir un utilisateur parmi la liste
        names = [u.get("name") for u in users_data]
        selected = st.selectbox("Choisir un utilisateur", names)
        user_dict = next((u for u in users_data if u.get("name") == selected), None)
        
        if user_dict:
            st.header(selected)
            # Affichage de la météo dynamique
            weather = get_weather()
            c1, c2 = st.columns([1,3])
            with c1: st.metric("Température", f"{weather['temperature']}°C", weather['icon'])
            with c2: 
                st.write(f"**{weather['description']}**")
                st.caption(weather.get('recommendation',''))
            
            # Métriques clés (KPIs) de l'utilisateur
            col1, col2, col3 = st.columns(3)
            col1.metric("Âge", user_dict.get("age"))
            col2.metric("Objectif", user_dict.get("goal"))
            col3.metric("Jours suivis", len(user_dict.get("daily_logs", [])))
            
            # Transformation des logs en DataFrame pour le tracé de courbes
            df = pd.DataFrame(user_dict.get("daily_logs", []))
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"])
                # Onglets pour séparer les types de graphiques
                tab1, tab2, tab3 = st.tabs(["📈 Évolution", "🏋️ Fréquence Sports", "🔥 Calories par Sport"])
                with tab1:
                    fig, ax = plt.subplots(figsize=(10,4))
                    ax.plot(df["date"], df["steps"], color="#00D4FF", marker="o")
                    st.pyplot(fig)
                with tab2:
                    counts = df["workout"].value_counts()
                    fig, ax = plt.subplots(figsize=(10,4))
                    sns.barplot(x=counts.values, y=counts.index, palette="viridis", ax=ax)
                    st.pyplot(fig)
                with tab3:
                    fig, ax = plt.subplots(figsize=(10,4))
                    sns.boxplot(data=df, x="workout", y="calories", palette="viridis", ax=ax)
                    st.pyplot(fig)

# ===================== STATISTIQUES GLOBALES =====================
elif page == "📊 Statistiques Globales":
    if not users_data:
        st.warning("Génère des profils d'abord")
    else:
        st.header("📊 Statistiques Globales")
        # Aplatissement des données (Flattening) : on fusionne les logs de tous les users
        all_logs = []
        for u in users_data:
            for log in u.get("daily_logs", []):
                all_logs.append({**log, "name": u.get("name"), "goal": u.get("goal")})
        df = pd.DataFrame(all_logs)
        
        # Affichage des métriques agrégées pour la communauté
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Utilisateurs", len(users_data))
        c2.metric("Moy. Pas/jour", f"{df['steps'].mean():.0f}")
        c3.metric("Moy. Calories", f"{df['calories'].mean():.0f}")
        c4.metric("Total Sessions", len(df))
        
        # Graphique en barres des objectifs communautaires
        st.subheader("Répartition des Objectifs")
        st.bar_chart(pd.Series([u.get("goal") for u in users_data]).value_counts())

# ===================== VISUALISATIONS =====================
elif page == "📈 Visualisations":
    if not users_data:
        st.warning("Génère des profils d'abord")
    else:
        st.header("📈 Visualisations Globales")
        # Ré-extraction des données globales
        all_logs = []
        for u in users_data:
            for log in u.get("daily_logs", []):
                all_logs.append({**log, "name": u.get("name")})
        df = pd.DataFrame(all_logs)
        df["date"] = pd.to_datetime(df["date"])
        
        # Visualisations complexes en onglets
        tab1, tab2, tab3 = st.tabs(["Évolution Globale", "Fréquence Sports", "Calories par Sport"])
        with tab1:
            # Graphique à double axe (Y1: Pas, Y2: Calories)
            daily = df.groupby("date")[["steps", "calories"]].mean().reset_index()
            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(daily["date"], daily["steps"], label="Pas")
            ax.twinx().plot(daily["date"], daily["calories"], color="red", label="Calories")
            st.pyplot(fig)
        with tab2:
            fig, ax = plt.subplots(figsize=(10,4))
            sns.barplot(x=df["workout"].value_counts().index, y=df["workout"].value_counts().values, ax=ax)
            st.pyplot(fig)
        with tab3:
            fig, ax = plt.subplots(figsize=(10,4))
            sns.boxplot(data=df, x="workout", y="calories", ax=ax)
            st.pyplot(fig)

# Pied de page informatif
st.caption("FitSync AI • Hackathon 2026")