"""Section « Données » de la barre latérale : import de fichiers et d'URL."""
import pandas as pd
import streamlit as st

from .fetch_url import fetch_url
from .import_sources import import_sources


def sidebar_import(offers: pd.DataFrame) -> pd.DataFrame:
    """Affiche l'import (fichiers, URL d'API, mode remplacer) et renvoie les offres à utiliser.

    Un SKU déjà présent est remplacé par la version importée.

    Args:
        offers: offres d'origine.

    Returns:
        Les offres d'origine, complétées ou remplacées par les imports.
    """
    with st.sidebar:
        st.header("Données")
        uploads = st.file_uploader("Importer des fichiers CSV / JSON", type=["csv", "json"],
                                   accept_multiple_files=True)
        api_url = st.text_input("…ou l'URL d'une API (JSON / CSV)",
                                placeholder="https://mon-api.com/offres")
        replace = st.toggle("Remplacer les données d'origine", value=False)
        # sources : couples (nom, contenu) de tout ce qui est importé.
        sources = [(f.name, f.getvalue()) for f in uploads or []]
        try:
            if api_url:
                sources.append(fetch_url(api_url))
            if sources:
                imported = import_sources(tuple(sources))
                offers = imported if replace else (
                    pd.concat([offers, imported], ignore_index=True)
                    .drop_duplicates(subset=["sku"], keep="last"))
                st.success(f"{len(imported)} offres importées depuis {len(sources)} source(s)")
        except Exception as exc:
            st.error(f"Import impossible : {exc}")
    return offers
