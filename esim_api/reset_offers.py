"""Retour aux données d'origine dans l'API."""
from . import store
from .config import ORIGIN_LABEL


def reset_offers() -> None:
    """Oublie tous les imports : l'API sert de nouveau les seules offres d'origine."""
    with store.lock:
        store.offers = store.base
        store.sources = [ORIGIN_LABEL]
