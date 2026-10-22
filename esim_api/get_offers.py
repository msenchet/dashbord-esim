"""Route GET /api/offers : liste des offres en JSON."""
from fastapi import Depends, Query

from esim import to_records

from . import store
from .apply_filters import apply_filters
from .config import DEFAULT_LIMIT, MAX_LIMIT, SortKey, SortOrder
from .get_filters import get_filters
from .models import OfferFilters


def get_offers(
    filters: OfferFilters = Depends(get_filters),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    offset: int = Query(0, ge=0),
    sort: SortKey = "price",
    order: SortOrder = "asc",
) -> dict:
    """Renvoie les offres filtrées, triées et paginées.

    Args:
        filters: filtres lus dans l'URL.
        limit: nombre maximal d'offres renvoyées.
        offset: nombre d'offres à sauter (pagination).
        sort: colonne de tri.
        order: « asc » (croissant) ou « desc » (décroissant).

    Returns:
        ``{total, limit, offset, offers: [...]}`` ; total compte toutes les offres filtrées.
    """
    # df : offres filtrées puis triées (valeurs manquantes en dernier).
    df = apply_filters(store.offers, filters)
    df = df.sort_values(sort, ascending=order == "asc", na_position="last")
    return {"total": len(df), "limit": limit, "offset": offset,
            "offers": to_records(df.iloc[offset:offset + limit])}
