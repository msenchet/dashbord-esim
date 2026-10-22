"""Nettoyage des données reçues par une route d'import."""
import pandas as pd
from fastapi import HTTPException

from esim import clean_offers, prepare_frame


def parse_import(frames: list[tuple[pd.DataFrame, str]]) -> pd.DataFrame:
    """Harmonise et nettoie les tableaux importés, ou renvoie une erreur 422 lisible.

    Args:
        frames: liste de couples (tableau brut, nom de la source).

    Returns:
        Les offres nettoyées, toutes sources réunies.

    Raises:
        HTTPException: 422 si les données sont illisibles ou ne contiennent aucune offre valide.
    """
    try:
        # prepared : chaque source avec ses colonnes renommées et son fournisseur complété.
        prepared = [prepare_frame(df, name) for df, name in frames]
        cleaned = clean_offers(pd.concat(prepared, ignore_index=True))
    except (ValueError, KeyError) as exc:
        raise HTTPException(422, f"Données illisibles : {exc}") from exc
    if cleaned.empty:
        raise HTTPException(
            422, "Aucune offre valide (prix manquant ou illisible sur toutes les lignes)")
    return cleaned
