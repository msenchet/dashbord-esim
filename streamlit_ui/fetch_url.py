"""Téléchargement mis en cache d'une URL d'API."""
import streamlit as st

from esim import fetch_public_url

from .config import URL_CACHE_SECONDS, URL_TIMEOUT_SECONDS


@st.cache_data(ttl=URL_CACHE_SECONDS, show_spinner="Appel de l'API…")
def fetch_url(url: str) -> tuple[str, bytes]:
    """Télécharge une API JSON ou un fichier CSV en ligne (réponse gardée 5 minutes).

    Seules les adresses publiques sont acceptées et la réponse est limitée à 20 Mo
    (voir esim.fetch_public_url), ce qui protège une application hébergée contre le SSRF.

    Args:
        url: adresse à télécharger.

    Returns:
        Le nom de fichier déduit de l'URL (« .json » ajouté si le serveur annonce du JSON)
        et le contenu brut.

    Raises:
        ValueError: adresse refusée ou réponse trop volumineuse.
        httpx.HTTPError: serveur injoignable ou réponse en erreur.
    """
    final_url, content_type, content = fetch_public_url(url, URL_TIMEOUT_SECONDS)
    # name : dernier segment du chemin de l'URL, sans paramètres.
    name = final_url.split("?")[0].rstrip("/").rsplit("/", 1)[-1] or "api"
    if "json" in content_type and not name.endswith(".json"):
        name += ".json"
    return name, content
