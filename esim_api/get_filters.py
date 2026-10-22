"""Lecture des filtres passés dans l'URL des routes d'export."""
from fastapi import Query

from .config import Kind
from .models import OfferFilters


def get_filters(
    provider: list[str] | None = Query(None, description="Un ou plusieurs fournisseurs"),
    country: list[str] | None = Query(None, description="Une ou plusieurs destinations"),
    validity: list[int] | None = Query(None, description="Durées en jours (7, 15, 30…)"),
    network: list[str] | None = Query(None, description="4G, 5G"),
    kind: Kind = "all",
    min_price: float | None = None,
    max_price: float | None = None,
    q: str | None = Query(None, description="Recherche texte"),
) -> OfferFilters:
    """Dépendance FastAPI : rassemble les paramètres d'URL en un objet OfferFilters.

    Exemple : ``/api/offers?provider=Holafly&kind=unlimited&max_price=40``.
    Chaque paramètre est décrit dans ``models.OfferFilters``.

    Returns:
        Les filtres demandés par le client.
    """
    return OfferFilters(provider=provider, country=country, validity=validity, network=network,
                        kind=kind, min_price=min_price, max_price=max_price, q=q)
