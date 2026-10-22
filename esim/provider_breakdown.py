"""Répartition des offres par fournisseur."""
import pandas as pd


def provider_breakdown(offers: pd.DataFrame) -> pd.DataFrame:
    """Calcule, pour chaque fournisseur, son volume d'offres, ses prix et son prix au Go.

    Args:
        offers: tableau nettoyé (éventuellement filtré) des offres.

    Returns:
        Un tableau indexé par fournisseur, trié du plus grand nombre d'offres au plus petit,
        avec les colonnes : offres, part_%, prix_moyen, prix_min, prix_max,
        offres_illimitees, prix_moyen_par_go (hors illimité).
    """
    # grouped : les offres regroupées par fournisseur.
    grouped = offers.groupby("provider")
    table = pd.DataFrame({
        "offres": grouped.size(),
        "part_%": grouped.size() / len(offers) * 100,
        "prix_moyen": grouped["price"].mean(),
        "prix_min": grouped["price"].min(),
        "prix_max": grouped["price"].max(),
        "offres_illimitees": grouped["is_unlimited"].sum().astype(int),
        "prix_moyen_par_go": grouped["price_per_gb"].mean(),
    })
    return table.sort_values("offres", ascending=False)
