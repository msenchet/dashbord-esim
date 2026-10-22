"""Dashboard Streamlit des offres eSIM.

Lancer : streamlit run app.py

Ce script enchaîne les étapes de la page ; chaque étape est une fonction du paquet
streamlit_ui/ (un fichier par fonction).
"""
import streamlit as st

from esim import compute_stats, provider_breakdown
from streamlit_ui.filter_offers import filter_offers
from streamlit_ui.get_offers import get_offers
from streamlit_ui.render_breakdown_table import render_breakdown_table
from streamlit_ui.render_exports import render_exports
from streamlit_ui.render_kpis import render_kpis
from streamlit_ui.render_offers_table import render_offers_table
from streamlit_ui.render_price_charts import render_price_charts
from streamlit_ui.render_provider_charts import render_provider_charts
from streamlit_ui.search_offers import search_offers
from streamlit_ui.sidebar_filters import sidebar_filters
from streamlit_ui.sidebar_import import sidebar_import

# Réglages de la page : doit être la première commande Streamlit.
st.set_page_config(page_title="Dashboard eSIM", page_icon="📶", layout="wide")

# offers : offres d'origine, complétées ou remplacées par les imports de la barre latérale.
offers = sidebar_import(get_offers())

# filters : choix de la barre latérale ; df : offres qui les respectent.
filters = sidebar_filters(offers)
df = filter_offers(offers, filters)

st.title("📶 Comparateur d'offres eSIM")
st.caption(f"{len(offers):,} offres de {offers['provider'].nunique()} fournisseurs, "
           f"issues de {offers['source_file'].nunique()} sources · prix en EUR".replace(",", " "))

if df.empty:
    st.warning("Aucune offre ne correspond aux filtres.")
    st.stop()

# ---------- Indicateurs ----------
render_kpis(compute_stats(df))
st.divider()

# ---------- Graphiques ----------
# breakdown : répartition par fournisseur, le fournisseur en colonne.
breakdown = provider_breakdown(df).reset_index()
render_provider_charts(breakdown)
render_price_charts(df)

# ---------- Tableaux et export ----------
render_breakdown_table(breakdown)
st.subheader("Toutes les offres")
# search : mots tapés ; table : offres affichées après la recherche.
search = st.text_input("Rechercher une offre", placeholder="ex. japon 5g -holafly",
                       help="Chaque mot est un critère (ET), une virgule donne des alternatives "
                            "(japon,corée), un « - » exclut un mot (-holafly).")
table = search_offers(df, search)
render_offers_table(table)
render_exports(table)
