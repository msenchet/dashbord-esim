"""Route GET /api/sources : sources de données chargées."""
from . import store


def get_sources() -> dict:
    """Indique combien d'offres sont servies et de quelles sources elles viennent.

    Returns:
        ``{total_offers, sources: [...]}``.
    """
    return {"total_offers": len(store.offers), "sources": store.sources}
