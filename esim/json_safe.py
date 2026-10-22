"""Conversion d'une valeur numpy en valeur acceptée par le JSON."""
import numpy as np


def json_safe(value):
    """Rend une valeur sérialisable en JSON : entiers numpy → int, NaN → None, réels arrondis.

    Args:
        value: valeur issue d'un calcul pandas/numpy.

    Returns:
        La valeur convertie (int, float arrondi à 4 décimales, None ou valeur d'origine).
    """
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return None if np.isnan(value) else round(float(value), 4)
    return value
