"""Nettoyage mis en cache des fichiers importés."""
import pandas as pd
import streamlit as st

from esim import clean_offers, prepare_frame, read_any


@st.cache_data(show_spinner="Import des données…")
def import_sources(files: tuple[tuple[str, bytes], ...]) -> pd.DataFrame:
    """Lit et nettoie des fichiers CSV/JSON importés (résultat mis en cache par contenu).

    Args:
        files: couples (nom du fichier, contenu en octets).

    Returns:
        Les offres importées, nettoyées.
    """
    # frames : un tableau harmonisé par fichier.
    frames = [prepare_frame(read_any(content, name), name) for name, content in files]
    return clean_offers(pd.concat(frames, ignore_index=True))
