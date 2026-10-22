"""Route GET /api/stats : indicateurs globaux."""
from fastapi import Depends

from esim import EXPENSIVE_THRESHOLD, compute_stats, json_safe

from . import store
from .apply_filters import apply_filters
from .get_filters import get_filters
from .models import OfferFilters


def get_stats(filters: OfferFilters = Depends(get_filters)) -> dict:
    """Renvoie les 6 statistiques et les KPIs bonus des offres filtrées.

    Args:
        filters: filtres lus dans l'URL.

    Returns:
        Les indicateurs (voir esim.compute_stats) et le seuil des offres chères,
        ou ``{"total_offers": 0}`` si aucune offre ne correspond.
    """
    df = apply_filters(store.offers, filters)
    if df.empty:
        return {"total_offers": 0}
    # stats : indicateurs convertis en valeurs JSON (NaN → null, réels arrondis).
    stats = {key: json_safe(value) for key, value in compute_stats(df).items()}
    return stats | {"expensive_threshold": EXPENSIVE_THRESHOLD}
