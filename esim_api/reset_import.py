"""Route DELETE /api/import : retour aux données d'origine."""
from .get_sources import get_sources
from .reset_offers import reset_offers


def reset_import() -> dict:
    """Annule tous les imports et renvoie les sources désormais chargées.

    Returns:
        ``{total_offers, sources}`` après remise à zéro.
    """
    reset_offers()
    return get_sources()
