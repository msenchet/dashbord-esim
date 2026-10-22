"""Application des filtres de la barre latérale."""
import pandas as pd

from .config import KIND_LIMITED, KIND_UNLIMITED


def filter_offers(offers: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Garde les offres qui respectent les filtres choisis.

    Args:
        offers: offres chargées.
        filters: choix renvoyés par sidebar_filters ; une liste vide ne filtre pas.

    Returns:
        Les offres retenues.
    """
    # mask : True pour chaque offre encore retenue.
    mask = offers["price"].between(*filters["price_range"])
    if filters["providers"]:
        mask &= offers["provider"].isin(filters["providers"])
    if filters["countries"]:
        mask &= offers["country_name"].isin(filters["countries"])
    if filters["validities"]:
        mask &= offers["validity_days"].isin(filters["validities"])
    if filters["networks"]:
        mask &= offers["network"].isin(filters["networks"])
    if filters["kind"] == KIND_LIMITED:
        mask &= ~offers["is_unlimited"]
    elif filters["kind"] == KIND_UNLIMITED:
        mask &= offers["is_unlimited"]
    return offers[mask]
