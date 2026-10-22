"""Préparation des offres au format compact injecté dans la page."""
import pandas as pd


def build_payload(offers: pd.DataFrame) -> dict:
    """Convertit les offres au format « colonnes » compact lu par decodeRaw (JavaScript).

    Fournisseurs et pays ne sont écrits qu'une fois ; chaque offre garde seulement leur index.

    Args:
        offers: offres nettoyées.

    Returns:
        Un dictionnaire de listes (voir la description de RAW dans site/js/donnees.js).
    """
    # providers / countries : valeurs uniques triées ; codes : code pays de chaque pays.
    providers = sorted(offers["provider"].unique())
    countries = sorted(offers["country_name"].unique())
    codes = offers.groupby("country_name")["country_code"].first()
    # p_index / c_index : position de chaque fournisseur et pays dans ces listes.
    p_index = {p: i for i, p in enumerate(providers)}
    c_index = {c: i for i, c in enumerate(countries)}
    return {
        "providers": providers,
        "countries": countries,
        "codes": [codes.get(c) for c in countries],
        "sku": offers["sku"].tolist(),
        "provider": offers["provider"].map(p_index).tolist(),
        "country": offers["country_name"].map(c_index).tolist(),
        "name": offers["product_name"].tolist(),
        "gb": [None if unlimited else round(float(gb), 3)
               for gb, unlimited in zip(offers["data_gb"], offers["is_unlimited"])],
        "validity": offers["validity_days"].astype(int).tolist(),
        "price": offers["price"].round(2).tolist(),
        "network": offers["network"].tolist(),
        "top_up": offers["top_up"].astype(int).tolist(),
    }
