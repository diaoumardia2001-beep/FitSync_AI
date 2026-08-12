import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import os
import sys

# Imports projet
from models.user import generate_fake_users, User
from models.workout import Workout
from utils.file_manager import save_users, load_users
from utils.weather import get_weather
from utils.weekly_report import generate_weekly_report
from utils.badges import check_badges, ALL_BADGES
from analysis.stats import (
    prepare_dataframe,
    anova_calories_by_workout,
    linear_regression_steps,
    ttest_before_after,
    weekly_analysis
)
from data.pipeline import run_full_pipeline

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="FitSync AI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background-color: #09090B;
    color: #FAFAFA;
}
[data-testid="stSidebar"] {
    background-color: #0F0F11;
    border-right: 1px solid #1F1F23;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1400px; }

.card {
    background: #111113;
    border: 1px solid #1F1F23;
    border-radius: 12px;
    padding: 24px;
    margin: 8px 0;
    transition: border-color 0.2s ease;
}
.card:hover { border-color: #3F3F46; }

.metric-box {
    background: #111113;
    border: 1px solid #1F1F23;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
}
.metric-box .val {
    font-size: 36px;
    font-weight: 800;
    color: #FAFAFA;
    letter-spacing: -1px;
    line-height: 1;
}
.metric-box .lbl {
    font-size: 12px;
    font-weight: 500;
    color: #71717A;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

.hero {
    padding: 48px 0 32px;
    text-align: center;
}
.hero h1 {
    font-size: 64px;
    font-weight: 900;
    letter-spacing: -3px;
    color: #FAFAFA;
    line-height: 1;
}
.hero h1 span { color: #22C55E; }
.hero p {
    font-size: 18px;
    color: #71717A;
    margin-top: 12px;
}

.section-title {
    font-size: 12px;
    font-weight: 600;
    color: #71717A;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1F1F23;
}

.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px;
}
.badge-green {
    background:#0F2A1A;
    color:#22C55E;
    border:1px solid #166534;
}
.badge-blue {
    background:#0C1929;
    color:#3B82F6;
    border:1px solid #1E3A5F;
}
.badge-yellow {
    background:#2A1F0A;
    color:#F59E0B;
    border:1px solid #92400E;
}
.badge-gray {
    background:#1A1A1A;
    color:#71717A;
    border:1px solid #2F2F35;
}

.stButton > button {
    background: #FAFAFA !important;
    color: #09090B !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stSelectbox > div > div {
    background: #111113 !important;
    border: 1px solid #1F1F23 !important;
    border-radius: 8px !important;
}
div[data-testid="stMetric"] {
    background: #111113;
    border: 1px solid #1F1F23;
    border-radius: 12px;
    padding: 16px 20px;
}
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PLOTLY LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#111113",
    plot_bgcolor="#111113",
    font=dict(
        family="Inter, sans-serif",
        color="#A1A1AA",
        size=12
    ),
    xaxis=dict(
        gridcolor="#1F1F23",
        linecolor="#1F1F23",
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        gridcolor="#1F1F23",
        linecolor="#1F1F23",
        showgrid=True,
        zeroline=False
    ),
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(
        bgcolor="#1F1F23",
        bordercolor="#2F2F35",
        font=dict(color="#FAFAFA", size=13)
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="#1F1F23"
    ),
    colorway=[
        "#22C55E", "#3B82F6", "#F59E0B",
        "#EF4444", "#8B5CF6", "#06B6D4"
    ]
)

CHART_CONFIG = {"displayModeBar": False}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_users_df(users_data):
    rows = []
    for u in users_data:
        for log in u.get("daily_logs", []):
            rows.append({
                "name": u["name"],
                "goal": u["goal"],
                "age": u["age"],
                "date": log["date"],
                "steps": log["steps"],
                "calories": log["calories"],
                "workout": log["workout"]
            })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df


def get_fit_score(user_dict):
    user = User(
        name=user_dict["name"],
        age=user_dict["age"],
        goal=user_dict["goal"]
    )
    user.daily_logs = user_dict["daily_logs"]
    workout = Workout(user)
    score, message = workout.calculate_fit_score()
    return score, message


def score_color(score):
    if score >= 80:
        return "#22C55E"
    elif score >= 60:
        return "#3B82F6"
    elif score >= 40:
        return "#F59E0B"
    return "#EF4444"


def score_label(score):
    if score >= 80:
        return "🏆 Excellent"
    elif score >= 60:
        return "💪 Bon"
    elif score >= 40:
        return "📈 Moyen"
    return "⚠️ Faible"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 16px 20px;
    border-bottom:1px solid #1F1F23;
    margin-bottom:8px;">
      <div style="display:flex;
      align-items:center; gap:10px;">
        <svg width="32" height="32"
        viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32"
          rx="8" fill="#22C55E"/>
          <path d="M6 16h4l3-6 5 12 3-6h5"
          stroke="white" stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"/>
        </svg>
        <div>
          <div style="font-size:16px;
          font-weight:800; color:#FAFAFA;
          letter-spacing:-0.3px;">FitSync AI</div>
          <div style="font-size:11px;
          color:#52525B; margin-top:1px;">
            v1.0 · Hackathon 2026
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p class='section-title'>Navigation</p>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "",
        options=[
            "🏠  Accueil",
            "🔬  Pipeline Données",
            "💪  Entraînement",
            "📊  Statistiques",
            "📈  Visualisations",
            "📅  Rapports & Badges"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <div style="padding:16px;
    background:#111113;
    border:1px solid #1F1F23;
    border-radius:12px;
    font-size:13px; color:#71717A;">
      <div style="color:#FAFAFA;
      font-weight:600; margin-bottom:8px;">
        👥 FitSync Masters
      </div>
      Rabiatou Ouedraogo<br>
      Dia Oumar<br>
      <div style="margin-top:8px;
      color:#52525B;">
        COT_GenAI 2026
      </div>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 1 — ACCUEIL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if page == "🏠  Accueil":
    st.markdown("""
    <div class="hero">
      <h1>FitSync <span>AI</span></h1>
      <p>Coach Fitness Intelligent ·
         Hackathon #1 · COT_GenAI 2026</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Générer des profils"):
            with st.spinner("Génération en cours..."):
                users = generate_fake_users(5)
                save_users(users)
            st.success("✅ 5 profils générés !")

    users_data = load_users()

    if not users_data:
        st.info(
            "👆 Cliquez sur 'Générer des profils' "
            "pour commencer"
        )
    else:
        # KPIs
        df = get_users_df(users_data)
        st.markdown("<div class='section-title'>"
                    "Vue d'ensemble</div>",
                    unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric(
                "👥 Utilisateurs",
                len(users_data)
            )
        with k2:
            st.metric(
                "👟 Moy. Pas/jour",
                f"{df['steps'].mean():,.0f}"
            )
        with k3:
            st.metric(
                "🔥 Moy. Calories",
                f"{df['calories'].mean():,.0f}"
            )
        with k4:
            scores = [
                get_fit_score(u)[0]
                for u in users_data
            ]
            st.metric(
                "🤖 FitScore Moyen",
                f"{np.mean(scores):.0f}/100"
            )

        # Cards utilisateurs
        st.markdown("<div class='section-title' "
                    "style='margin-top:24px'>"
                    "Profils</div>",
                    unsafe_allow_html=True)

        cols = st.columns(2)
        for i, user_dict in enumerate(users_data):
            score, msg = get_fit_score(user_dict)
            color = score_color(score)
            label = score_label(score)

            with cols[i % 2]:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    domain={"x": [0, 1], "y": [0, 1]},
                    gauge={
                        "axis": {
                            "range": [0, 100],
                            "tickcolor": "#71717A"
                        },
                        "bar": {"color": color},
                        "bgcolor": "#1F1F23",
                        "bordercolor": "#1F1F23",
                        "steps": [
                            {"range": [0, 40],
                             "color": "#2A0F0F"},
                            {"range": [40, 60],
                             "color": "#2A1F0A"},
                            {"range": [60, 80],
                             "color": "#0C1929"},
                            {"range": [80, 100],
                             "color": "#0F2A1A"}
                        ]
                    },
                    title={
                        "text": (
                            f"{user_dict['name']}<br>"
                            f"<span style='font-size:12px'>"
                            f"{label}</span>"
                        ),
                        "font": {"color": "#FAFAFA"}
                    },
                    number={"font": {"color": color}}
                ))
                fig.update_layout(
                    **{**PLOTLY_LAYOUT,
                       "height": 250,
                       "margin": dict(
                           l=20, r=20, t=60, b=20
                       )}
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config=CHART_CONFIG
                )
                st.markdown(
                    f"<div style='text-align:center;"
                    f"color:#71717A; font-size:13px;"
                    f"margin-top:-16px;'>"
                    f"🎯 {user_dict['goal']} · "
                    f"{user_dict['age']} ans</div>",
                    unsafe_allow_html=True
                )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 2 — PIPELINE DONNÉES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "🔬  Pipeline Données":
    st.markdown(
        "<h2 style='color:#FAFAFA; "
        "font-weight:800; letter-spacing:-1px;'>"
        "🔬 Pipeline de Données</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#71717A;'>"
        "Collecte → Nettoyage → Prétraitement</p>",
        unsafe_allow_html=True
    )

    if st.button("🚀 Lancer le pipeline complet"):
        with st.spinner(
            "Pipeline en cours... "
            "(50 users × 30 jours)"
        ):
            df_processed, report = run_full_pipeline(
                n_users=50, n_days=30
            )

        st.success("✅ Pipeline terminé !")

        # Métriques nettoyage
        st.markdown(
            "<div class='section-title'>"
            "Résultats du nettoyage</div>",
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            missing_before = report.get("missing_before", 0)
            missing_after = report.get("missing_after", 0)
            st.metric(
                "❌ Valeurs manquantes",
                missing_after,
                delta=f"{missing_after - missing_before}"
            )
        with c2:
            st.metric(
                "🗑️ Doublons supprimés",
                report.get("duplicates_removed", 0)
            )
        with c3:
            total_out = sum(
                v for k, v in report.items()
                if k.startswith("outliers_")
            )
            st.metric("📊 Outliers traités", total_out)
        with c4:
            st.metric(
                "✨ Features créées", 6
            )

        # Aperçu données
        st.markdown(
            "<div class='section-title' "
            "style='margin-top:24px;'>"
            "Aperçu des données prétraitées</div>",
            unsafe_allow_html=True
        )
        st.dataframe(
            df_processed.head(20),
            use_container_width=True
        )

        # Statistiques descriptives
        st.markdown(
            "<div class='section-title'>"
            "Statistiques descriptives</div>",
            unsafe_allow_html=True
        )
        numeric_cols = [
            "steps", "calories",
            "heart_rate", "sleep_hours"
        ]
        st.dataframe(
            df_processed[numeric_cols].describe().round(2),
            use_container_width=True
        )

        # Heatmap corrélations
        st.markdown(
            "<div class='section-title'>"
            "Matrice de corrélation</div>",
            unsafe_allow_html=True
        )
        corr = df_processed[numeric_cols].corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Corrélations entre variables"
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config=CHART_CONFIG
        )

    else:
        st.markdown("""
        <div class='card'>
          <h4 style='color:#FAFAFA; margin:0 0 8px;'>
            Ce que fait le pipeline
          </h4>
          <p style='color:#71717A; margin:0;'>
            1. 📥 <b style='color:#FAFAFA;'>
            Collecte</b> — Génère 50 utilisateurs
            avec des données brutes imparfaites<br>
            2. 🧹 <b style='color:#FAFAFA;'>
            Nettoyage</b> — Traite les valeurs
            manquantes, doublons et outliers<br>
            3. ⚙️ <b style='color:#FAFAFA;'>
            Prétraitement</b> — Normalisation,
            encodage et feature engineering<br>
            4. 💾 <b style='color:#FAFAFA;'>
            Sauvegarde</b> — CSV + JSON à chaque étape
          </p>
        </div>
        """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 3 — ENTRAÎNEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "💪  Entraînement":
    st.markdown(
        "<h2 style='color:#FAFAFA; "
        "font-weight:800; letter-spacing:-1px;'>"
        "💪 Plans d'Entraînement</h2>",
        unsafe_allow_html=True
    )

    users_data = load_users()
    if not users_data:
        st.warning(
            "⚠️ Allez sur Accueil pour "
            "générer des utilisateurs"
        )
    else:
        user_names = [u["name"] for u in users_data]
        selected = st.selectbox(
            "Choisir un utilisateur",
            user_names
        )
        user_dict = next(
            u for u in users_data
            if u["name"] == selected
        )

        # Météo + Profil + Score
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                "<div class='section-title'>"
                "Profil</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"""
            <div class='card'>
              <div style='font-size:24px;
              font-weight:800; color:#FAFAFA;'>
                {user_dict['name']}
              </div>
              <div style='color:#71717A;
              margin-top:8px; font-size:14px;'>
                🎯 {user_dict['goal']}<br>
                📅 {user_dict['age']} ans<br>
                📋 {len(user_dict['daily_logs'])} logs
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(
                "<div class='section-title'>"
                "Météo du jour — Abidjan</div>",
                unsafe_allow_html=True
            )
            weather = get_weather()
            cond = weather["condition"]
            if cond == "rain":
                st.error(
                    f"{weather['icon']} "
                    f"{weather['description']} · "
                    f"{weather['temperature']}°C"
                )
            elif cond == "hot":
                st.warning(
                    f"{weather['icon']} "
                    f"{weather['description']} · "
                    f"{weather['temperature']}°C"
                )
            else:
                st.success(
                    f"{weather['icon']} "
                    f"{weather['description']} · "
                    f"{weather['temperature']}°C"
                )
            st.caption(weather["recommendation"])

        with col3:
            score, msg = get_fit_score(user_dict)
            color = score_color(score)
            st.markdown(
                "<div class='section-title'>"
                "FitScore</div>",
                unsafe_allow_html=True
            )
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": color},
                    "bgcolor": "#1F1F23",
                    "bordercolor": "#1F1F23"
                },
                number={"font": {"color": color}}
            ))
            fig.update_layout(
                **{**PLOTLY_LAYOUT,
                   "height": 180,
                   "margin": dict(
                       l=20, r=20, t=20, b=20
                   )}
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                config=CHART_CONFIG
            )
            st.caption(msg)

        # Recommandation
        user = User(
            name=user_dict["name"],
            age=user_dict["age"],
            goal=user_dict["goal"]
        )
        user.daily_logs = user_dict["daily_logs"]
        workout = Workout(user)
        plan = workout.generate_plan(
            weather_condition=weather["condition"]
        )

        st.markdown(
            "<div class='section-title' "
            "style='margin-top:24px;'>"
            "Recommandation du jour</div>",
            unsafe_allow_html=True
        )
        st.info(
            f"**{plan['recommendation']}**\n\n"
            f"Niveau : {plan['level']} · "
            f"Moy. pas : {plan['avg_steps']:,} · "
            f"Moy. cal : {plan['avg_calories']:,}"
        )

        # Badges
        with st.expander("🏅 Badges obtenus"):
            earned, not_earned = check_badges(
                user_dict, score
            )
            if earned:
                cols = st.columns(3)
                for i, key in enumerate(earned):
                    badge = ALL_BADGES[key]
                    with cols[i % 3]:
                        st.markdown(
                            f"<div class='badge-pill "
                            f"badge-green'>"
                            f"{badge['icon']} "
                            f"{badge['name']}</div>",
                            unsafe_allow_html=True
                        )
            else:
                st.caption(
                    "Aucun badge obtenu pour l'instant"
                )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 4 — STATISTIQUES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📊  Statistiques":
    st.markdown(
        "<h2 style='color:#FAFAFA; "
        "font-weight:800; letter-spacing:-1px;'>"
        "📊 Analyse Statistique</h2>",
        unsafe_allow_html=True
    )

    users_data = load_users()
    if not users_data:
        st.warning("⚠️ Générez des utilisateurs d'abord")
    else:
        df = prepare_dataframe(users_data)

        # ANOVA
        st.markdown(
            "<div class='section-title'>"
            "ANOVA — Calories par workout</div>",
            unsafe_allow_html=True
        )
        groups = [
            g["calories"].values
            for _, g in df.groupby("workout")
            if len(g) > 1
        ]
        from scipy import stats as sp
        f_stat, p_value = sp.f_oneway(*groups)

        a1, a2, a3 = st.columns(3)
        with a1:
            st.metric("F-statistique", f"{f_stat:.4f}")
        with a2:
            st.metric("P-valeur", f"{p_value:.4f}")
        with a3:
            st.metric(
                "Résultat",
                "Significatif ✅"
                if p_value < 0.05
                else "Non significatif ❌"
            )

        fig = px.bar(
            df.groupby("workout")[
                "calories"
            ].mean().reset_index(),
            x="workout",
            y="calories",
            title="Calories moyennes par type de workout",
            labels={
                "workout": "Workout",
                "calories": "Calories moyennes"
            }
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config=CHART_CONFIG
        )

        st.divider()

        # Régression linéaire
        st.markdown(
            "<div class='section-title'>"
            "Régression linéaire — "
            "Prédiction des pas</div>",
            unsafe_allow_html=True
        )

        df_reg = df.copy().sort_values("date")
        df_reg["day_number"] = (
            df_reg["date"] - df_reg["date"].min()
        ).dt.days
        daily = df_reg.groupby("day_number")[
            "steps"
        ].mean().reset_index()

        slope, intercept, r_value, p_val, _ = (
            sp.linregress(
                daily["day_number"], daily["steps"]
            )
        )

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Pente", f"{slope:.2f} pas/jour")
        with r2:
            st.metric("R²", f"{r_value**2:.4f}")
        with r3:
            trend = "📈 Hausse" if slope > 0 else "📉 Baisse"
            st.metric("Tendance", trend)

        # Graphique régression
        daily["predicted"] = (
            intercept + slope * daily["day_number"]
        )
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=daily["day_number"],
            y=daily["steps"],
            mode="markers",
            name="Données réelles",
            marker=dict(color="#3B82F6", size=6)
        ))
        fig2.add_trace(go.Scatter(
            x=daily["day_number"],
            y=daily["predicted"],
            mode="lines",
            name="Tendance",
            line=dict(color="#22C55E", width=2)
        ))
        fig2.update_layout(
            **{**PLOTLY_LAYOUT,
               "title": "Évolution des pas + tendance"}
        )
        st.plotly_chart(
            fig2,
            use_container_width=True,
            config=CHART_CONFIG
        )

        st.divider()

        # T-test
        st.markdown(
            "<div class='section-title'>"
            "T-test — Strength Training vs HIIT</div>",
            unsafe_allow_html=True
        )
        strength = df[
            df["workout"] == "Strength Training"
        ]["calories"].values
        hiit = df[
            df["workout"] == "HIIT"
        ]["calories"].values

        if len(strength) > 0 and len(hiit) > 0:
            min_s = min(len(strength), len(hiit))
            t_stat, t_pval = sp.ttest_rel(
                strength[:min_s], hiit[:min_s]
            )

            t1, t2, t3, t4 = st.columns(4)
            with t1:
                st.metric(
                    "Moy. Strength",
                    f"{np.mean(strength):.0f} cal"
                )
            with t2:
                st.metric(
                    "Moy. HIIT",
                    f"{np.mean(hiit):.0f} cal"
                )
            with t3:
                st.metric(
                    "T-statistique",
                    f"{t_stat:.4f}"
                )
            with t4:
                st.metric("P-valeur", f"{t_pval:.4f}")

            fig3 = px.box(
                df[df["workout"].isin(
                    ["Strength Training", "HIIT"]
                )],
                x="workout",
                y="calories",
                title="Distribution calories : "
                      "Strength vs HIIT",
                color="workout"
            )
            fig3.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(
                fig3,
                use_container_width=True,
                config=CHART_CONFIG
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 5 — VISUALISATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📈  Visualisations":
    st.markdown(
        "<h2 style='color:#FAFAFA; "
        "font-weight:800; letter-spacing:-1px;'>"
        "📈 Visualisations</h2>",
        unsafe_allow_html=True
    )

    users_data = load_users()
    if not users_data:
        st.warning("⚠️ Générez des utilisateurs d'abord")
    else:
        df = get_users_df(users_data)

        # Filtres
        f1, f2 = st.columns(2)
        with f1:
            selected_user = st.selectbox(
                "Filtrer par utilisateur",
                ["Tous"] + [
                    u["name"] for u in users_data
                ]
            )
        with f2:
            selected_goal = st.selectbox(
                "Filtrer par objectif",
                ["Tous"] + list(df["goal"].unique())
            )

        df_filtered = df.copy()
        if selected_user != "Tous":
            df_filtered = df_filtered[
                df_filtered["name"] == selected_user
            ]
        if selected_goal != "Tous":
            df_filtered = df_filtered[
                df_filtered["goal"] == selected_goal
            ]

        # Graphique 1 — Pas & Calories
        daily = df_filtered.groupby("date")[
            ["steps", "calories"]
        ].mean().reset_index()

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=daily["date"], y=daily["steps"],
            name="Pas", mode="lines+markers",
            line=dict(color="#22C55E", width=2),
            marker=dict(size=4)
        ))
        fig1.add_trace(go.Scatter(
            x=daily["date"], y=daily["calories"],
            name="Calories", mode="lines+markers",
            line=dict(color="#EF4444", width=2),
            marker=dict(size=4),
            yaxis="y2"
        ))
        fig1.update_layout(
            **{**PLOTLY_LAYOUT,
               "title": "👟 Pas & 🔥 Calories par jour",
               "yaxis2": dict(
                   overlaying="y",
                   side="right",
                   gridcolor="#1F1F23",
                   showgrid=False
               )}
        )
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config=CHART_CONFIG
        )

        # Graphique 2 & 3 côte à côte
        col1, col2 = st.columns(2)

        with col1:
            workout_counts = (
                df_filtered["workout"].value_counts()
            )
            fig2 = px.bar(
                x=workout_counts.values,
                y=workout_counts.index,
                orientation="h",
                title="🏋️ Fréquence des workouts",
                labels={"x": "Séances", "y": ""}
            )
            fig2.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(
                fig2,
                use_container_width=True,
                config=CHART_CONFIG
            )

        with col2:
            fig3 = px.box(
                df_filtered,
                x="workout",
                y="calories",
                title="📊 Calories par workout",
                color="workout"
            )
            fig3.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(
                fig3,
                use_container_width=True,
                config=CHART_CONFIG
            )

        # Graphique 4 — Donut
        goal_counts = df_filtered.groupby(
            "goal"
        )["name"].nunique().reset_index()

        fig4 = px.pie(
            goal_counts,
            values="name",
            names="goal",
            title="🎯 Distribution des objectifs",
            hole=0.5
        )
        fig4.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(
            fig4,
            use_container_width=True,
            config=CHART_CONFIG
        )

        # Graphique 5 — Heatmap activité
        df_heat = df_filtered.copy()
        df_heat["week"] = df_heat[
            "date"
        ].dt.isocalendar().week
        df_heat["day"] = df_heat["date"].dt.day_name()
        pivot = df_heat.pivot_table(
            values="steps",
            index="day",
            columns="week",
            aggfunc="mean"
        ).fillna(0)

        fig5 = px.imshow(
            pivot,
            title="🗓️ Heatmap activité "
                  "(Jours × Semaines)",
            color_continuous_scale="Greens",
            labels={"color": "Pas moyens"}
        )
        fig5.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(
            fig5,
            use_container_width=True,
            config=CHART_CONFIG
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 6 — RAPPORTS & BADGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📅  Rapports & Badges":
    st.markdown(
        "<h2 style='color:#FAFAFA; "
        "font-weight:800; letter-spacing:-1px;'>"
        "📅 Rapports & Badges</h2>",
        unsafe_allow_html=True
    )

    users_data = load_users()
    if not users_data:
        st.warning("⚠️ Générez des utilisateurs d'abord")
    else:
        selected = st.selectbox(
            "Choisir un utilisateur",
            [u["name"] for u in users_data]
        )
        user_dict = next(
            u for u in users_data
            if u["name"] == selected
        )
        score, msg = get_fit_score(user_dict)
        logs = user_dict.get("daily_logs", [])
        last_7 = logs[:7]

        # Métriques hebdo
        st.markdown(
            "<div class='section-title'>"
            "Rapport hebdomadaire</div>",
            unsafe_allow_html=True
        )

        total_steps = sum(
            l["steps"] for l in last_7
        )
        total_cal = sum(
            l["calories"] for l in last_7
        )
        best = max(last_7, key=lambda l: l["steps"])
        worst = min(last_7, key=lambda l: l["steps"])
        workouts = [l["workout"] for l in last_7]
        fav = max(set(workouts), key=workouts.count)

        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("👟 Total pas", f"{total_steps:,}")
        with m2:
            st.metric("🔥 Total cal", f"{total_cal:,}")
        with m3:
            st.metric("🏋️ Séances", len(last_7))
        with m4:
            st.metric("💪 Favori", fav)
        with m5:
            st.metric("🏆 Meilleur", best["date"])

        # Graphique 7 derniers jours
        df_7 = pd.DataFrame(last_7)
        df_7["date"] = pd.to_datetime(df_7["date"])
        df_7 = df_7.sort_values("date")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_7["date"],
            y=df_7["steps"],
            name="Pas",
            marker_color="#22C55E",
            opacity=0.8
        ))
        fig.add_trace(go.Scatter(
            x=df_7["date"],
            y=df_7["calories"],
            name="Calories",
            mode="lines+markers",
            line=dict(color="#EF4444", width=2),
            yaxis="y2"
        ))
        fig.update_layout(
            **{**PLOTLY_LAYOUT,
               "title": "Activité des 7 derniers jours",
               "yaxis2": dict(
                   overlaying="y",
                   side="right",
                   gridcolor="#1F1F23",
                   showgrid=False
               )}
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            config=CHART_CONFIG
        )

        # Badges
        st.markdown(
            "<div class='section-title' "
            "style='margin-top:24px;'>"
            "Badges</div>",
            unsafe_allow_html=True
        )

        earned, not_earned = check_badges(
            user_dict, score
        )

        st.markdown(
            f"**{len(earned)}/{len(ALL_BADGES)} "
            f"badges obtenus**"
        )

        progress = len(earned) / len(ALL_BADGES)
        st.progress(progress)

        # Badges obtenus
        if earned:
            st.markdown("**✅ Obtenus :**")
            cols = st.columns(3)
            for i, key in enumerate(earned):
                badge = ALL_BADGES[key]
                with cols[i % 3]:
                    st.markdown(
                        f"<div class='card' "
                        f"style='text-align:center;"
                        f"padding:16px;'>"
                        f"<div style='font-size:28px;'>"
                        f"{badge['icon']}</div>"
                        f"<div style='color:#FAFAFA;"
                        f"font-weight:600; "
                        f"font-size:13px;"
                        f"margin-top:8px;'>"
                        f"{badge['name']}</div>"
                        f"<div style='color:#71717A;"
                        f"font-size:11px;"
                        f"margin-top:4px;'>"
                        f"{badge['desc']}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        # Badges non obtenus
        if not_earned:
            st.markdown("**🔒 À débloquer :**")
            cols = st.columns(3)
            for i, key in enumerate(not_earned):
                badge = ALL_BADGES[key]
                with cols[i % 3]:
                    st.markdown(
                        f"<div class='card' "
                        f"style='text-align:center;"
                        f"padding:16px;"
                        f"opacity:0.4;'>"
                        f"<div style='font-size:28px;'>"
                        f"⬜</div>"
                        f"<div style='color:#71717A;"
                        f"font-weight:600;"
                        f"font-size:13px;"
                        f"margin-top:8px;'>"
                        f"{badge['name']}</div>"
                        f"<div style='color:#52525B;"
                        f"font-size:11px;"
                        f"margin-top:4px;'>"
                        f"{badge['desc']}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        # Export
        st.markdown(
            "<div class='section-title' "
            "style='margin-top:24px;'>"
            "Export</div>",
            unsafe_allow_html=True
        )

        export_data = {
            "user": selected,
            "fit_score": score,
            "score_message": msg,
            "weekly_stats": {
                "total_steps": total_steps,
                "total_calories": total_cal,
                "sessions": len(last_7),
                "favorite_workout": fav
            },
            "badges_earned": earned,
            "badges_count": f"{len(earned)}"
                            f"/{len(ALL_BADGES)}"
        }

        st.download_button(
            label="📥 Télécharger rapport JSON",
            data=json.dumps(
                export_data, indent=2,
                ensure_ascii=False
            ),
            file_name=f"rapport_{selected}.json",
            mime="application/json"
        )