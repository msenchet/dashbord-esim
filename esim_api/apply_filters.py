"""Application des filtres de l'API à un tableau d'offres."""
import pandas as pd

from .models import OfferFilters


def apply_filters(df: pd.DataFrame, filters: OfferFilters) -> pd.DataFrame:
    """Garde les offres qui respectent tous les filtres demandés.

    Args:
        df: offres à filtrer.
        filters: filtres lus dans l'URL ; un champ vide ne filtre pas.

    Returns:
        Les offres retenues.
    """
    # mask : True pour chaque offre encore retenue après les filtres déjà appliqués.
    mask = pd.Series(True, index=df.index)
    if filters.provider:
        mask &= df["provider"].str.lower().isin([v.lower() for v in filters.provider])
    if filters.country:
        # wanted : destinations demandées, en minuscules (noms ou codes pays).
        wanted = [v.lower() for v in filters.country]
        mask &= (df["country_name"].str.lower().isin(wanted)
                 | df["country_code"].fillna("").str.lower().isin(wanted))
    if filters.validity:
        mask &= df["validity_days"].isin(filters.validity)
    if filters.network:
        mask &= df["network"].str.lower().isin([v.lower() for v in filters.network])
    if filters.kind != "all":
        mask &= df["is_unlimited"] == (filters.kind == "unlimited")
    if filters.min_price is not None:
        mask &= df["price"] >= filters.min_price
    if filters.max_price is not None:
        mask &= df["price"] <= filters.max_price
    if filters.q:
        # haystack : texte dans lequel on cherche q (fournisseur, offre, destination, réseau).
        haystack = (df["provider"] + " " + df["product_name"] + " "
                    + df["country_name"] + " " + df["network"])
        mask &= haystack.str.contains(filters.q, case=False, regex=False)
    return df[mask.fillna(False)]
