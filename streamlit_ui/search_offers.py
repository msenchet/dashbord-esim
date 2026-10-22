"""Recherche à plusieurs mots dans les offres."""
import pandas as pd

from .config import SEARCH_COLUMNS


def search_offers(df: pd.DataFrame, search: str) -> pd.DataFrame:
    """Garde les offres qui contiennent tous les mots tapés.

    Chaque mot est un critère (ET), une virgule donne des alternatives (japon,corée)
    et un « - » devant un mot l'exclut (-holafly).

    Args:
        df: offres retenues par les filtres.
        search: texte tapé dans la recherche.

    Returns:
        Les offres correspondantes (toutes si la recherche est vide).
    """
    if not search:
        return df
    # haystack : texte de chaque offre, en minuscules, dans lequel on cherche.
    haystack = df[SEARCH_COLUMNS].astype(str).agg(" ".join, axis=1).str.lower()
    mask = pd.Series(True, index=df.index)
    for word in search.lower().split():
        exclude = word.startswith("-") and len(word) > 1
        alternatives = [w for w in word.lstrip("-").split(",") if w]
        if not alternatives:
            continue
        # hit : offres qui contiennent au moins une des alternatives.
        hit = pd.concat([haystack.str.contains(w, regex=False) for w in alternatives],
                        axis=1).any(axis=1)
        mask &= ~hit if exclude else hit
    return df[mask]
