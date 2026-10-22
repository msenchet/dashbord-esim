"""Téléchargement mis en cache d'une URL d'API."""
import httpx
import streamlit as st

from .config import URL_CACHE_SECONDS, URL_TIMEOUT_SECONDS


@st.cache_data(ttl=URL_CACHE_SECONDS, show_spinner="Appel de l'API…")
def fetch_url(url: str) -> tuple[str, bytes]:
    """Télécharge une API JSON ou un fichier CSV en ligne (réponse gardée 5 minutes).

    Args:
        url: adresse à télécharger.

    Returns:
        Le nom de fichier déduit de l'URL (« .json » ajouté si le serveur annonce du JSON)
        et le contenu brut.

    Raises:
        httpx.HTTPError: si l'URL est injoignable ou répond une erreur.
    """
    resp = httpx.get(url, timeout=URL_TIMEOUT_SECONDS, follow_redirects=True)
    resp.raise_for_status()
    # name : dernier segment du chemin de l'URL, sans paramètres.
    name = url.split("?")[0].rstrip("/").rsplit("/", 1)[-1] or "api"
    if "json" in resp.headers.get("content-type", "") and not name.endswith(".json"):
        name += ".json"
    return name, resp.content
