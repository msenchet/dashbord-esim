"""Conversion d'un prix écrit librement en nombre décimal."""
import re

import numpy as np
import pandas as pd


def parse_price(value) -> float:
    """Convertit un prix en float : « 12,45 € », « €12.45 », « 1 234,50 » ou 12.45 → 12.45.

    Args:
        value: prix brut (texte, nombre ou valeur manquante).

    Returns:
        Le prix en float, ou NaN s'il est illisible.
    """
    if pd.isna(value):
        return np.nan
    # text : le prix sans espaces (normaux ou insécables) ni symbole monétaire.
    text = str(value).replace(" ", "").replace(" ", "")
    text = re.sub(r"[^\d,.\-]", "", text)
    if "," in text and "." in text:
        # Les deux séparateurs sont présents : le dernier est le séparateur décimal.
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    else:
        # Une virgule seule est un séparateur décimal à la française.
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return np.nan
