"""Lecture d'une colonne texte nettoyée."""
import pandas as pd


def text_column(offers: pd.DataFrame, col: str) -> pd.Series:
    """Renvoie une colonne en texte, sans espaces autour, les vides devenant manquants.

    Args:
        offers: tableau des offres.
        col: nom de la colonne voulue.

    Returns:
        La colonne nettoyée, ou une colonne entièrement manquante si elle n'existe pas.
    """
    if col not in offers.columns:
        return pd.Series(pd.NA, index=offers.index, dtype="string")
    return offers[col].astype("string").str.strip().replace("", pd.NA)
