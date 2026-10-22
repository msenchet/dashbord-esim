"""Chargement mis en cache des offres d'origine."""
import pandas as pd
import streamlit as st

from esim import load_offers


@st.cache_data
def get_offers() -> pd.DataFrame:
    """Charge les 18 CSV d'origine une seule fois par session de serveur (cache Streamlit).

    Returns:
        Les offres nettoyées.
    """
    return load_offers()
