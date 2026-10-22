"""Route GET /api/providers : répartition par fournisseur."""
from fastapi import Depends

from esim import json_safe, provider_breakdown

from . import store
from .apply_filters import apply_filters
from .get_filters import get_filters
from .models import OfferFilters


def get_providers(filters: OfferFilters = Depends(get_filters)) -> list[dict]:
    """Renvoie, pour chaque fournisseur, ses offres, ses prix et son prix moyen au Go.

    Args:
        filters: filtres lus dans l'URL.

    Returns:
        Une ligne par fournisseur (voir esim.provider_breakdown), liste vide si aucune offre.
    """
    df = apply_filters(store.offers, filters)
    if df.empty:
        return []
    # table : répartition avec le fournisseur en colonne plutôt qu'en index.
    table = provider_breakdown(df).reset_index()
    return [{key: json_safe(value) for key, value in row.items()}
            for row in table.to_dict(orient="records")]
