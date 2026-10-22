"""Route GET / : présentation rapide de l'API."""
from . import store


def root() -> dict:
    """Indique où trouver la documentation et combien d'offres sont chargées.

    Returns:
        Nom de l'API, lien vers /docs, nombre d'offres et sources chargées.
    """
    return {"api": "eSIM", "docs": "/docs", "offres": len(store.offers), "sources": store.sources}
