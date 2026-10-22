"""Route POST /api/import/json : import d'offres envoyées en JSON."""
from fastapi import Body, HTTPException

from esim import records_from_json

from .config import Mode
from .merge_offers import merge_offers
from .parse_import import parse_import

# Exemple affiché dans la documentation interactive (/docs).
EXAMPLE = {"offers": [{"provider": "MonOpérateur", "country_name": "Japon", "data_gb": 10,
                       "validity_days": 15, "price": 19.9}]}


def import_json(payload: list[dict] | dict = Body(..., examples=[EXAMPLE]),
                mode: Mode = "append", source: str = "import-json") -> dict:
    """Importe une liste d'offres ou un objet ``{"offers": [...]}`` envoyé dans le corps.

    Args:
        payload: offres envoyées en JSON.
        mode: « append » pour ajouter, « replace » pour remplacer les données.
        source: nom de la source affiché dans /api/sources.

    Returns:
        Le bilan de l'import (voir merge_offers).

    Raises:
        HTTPException: 422 si le JSON ne contient pas de liste d'offres valides.
    """
    try:
        df = records_from_json(payload)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return merge_offers(parse_import([(df, source)]), mode, source)
