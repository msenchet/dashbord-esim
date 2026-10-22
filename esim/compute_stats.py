"""Calcul des indicateurs globaux."""
import pandas as pd

from .config import EXPENSIVE_THRESHOLD


def compute_stats(offers: pd.DataFrame) -> dict:
    """Calcule les 6 statistiques demandées et les KPIs bonus.

    La data moyenne et le prix moyen au Go excluent les forfaits illimités,
    pour ne pas fausser les moyennes.

    Args:
        offers: tableau nettoyé (éventuellement filtré) des offres.

    Returns:
        Un dictionnaire : total_offers, offers_over_100, price_min, price_max, price_mean,
        data_mean_gb, unlimited_offers, providers, price_per_gb_mean.
    """
    # limited : offres à volume fini, seules prises en compte pour les moyennes de data.
    limited = offers[~offers["is_unlimited"]]
    return {
        "total_offers": len(offers),
        "offers_over_100": int((offers["price"] > EXPENSIVE_THRESHOLD).sum()),
        "price_min": offers["price"].min(),
        "price_max": offers["price"].max(),
        "price_mean": offers["price"].mean(),
        "data_mean_gb": limited["data_gb"].mean(),
        "unlimited_offers": int(offers["is_unlimited"].sum()),
        "providers": offers["provider"].nunique(),
        "price_per_gb_mean": limited["price_per_gb"].mean(),
    }
