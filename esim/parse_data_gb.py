"""Lecture du volume de data d'une offre (en Go) et détection de l'illimité."""
import numpy as np
import pandas as pd

from .config import UNIT_TO_GB, UNLIMITED_WORDS, VOLUME_RE
from .parse_price import parse_price


def parse_data_gb(gb_value, display_value=None) -> tuple[float, bool]:
    """Renvoie le volume en Go et indique si le forfait est illimité.

    La colonne numérique ``data_gb`` est prioritaire ; à défaut on lit le libellé
    (« 500 Mo », « 3 Go »). Un forfait illimité a un volume NaN.

    Args:
        gb_value: valeur de la colonne data_gb (nombre, texte avec unité ou vide).
        display_value: libellé affiché, par exemple « 3 Go » ou « Illimité ».

    Returns:
        Un couple (volume_en_go, est_illimite).
    """
    for raw in (display_value, gb_value):
        if isinstance(raw, str) and UNLIMITED_WORDS.search(raw):
            return np.nan, True

    if not pd.isna(gb_value) and str(gb_value).strip():
        # number : la valeur numérique ; unit_match : l'unité éventuellement écrite à côté.
        number = parse_price(gb_value)
        unit_match = VOLUME_RE.search(str(gb_value))
        unit = (unit_match.group(2) or "go").lower() if unit_match else "go"
        if not np.isnan(number):
            return number * UNIT_TO_GB[unit], False

    if isinstance(display_value, str):
        # match : nombre (groupe 1) et unité (groupe 2) trouvés dans le libellé.
        match = VOLUME_RE.search(display_value)
        if match:
            number = float(match.group(1).replace(",", "."))
            unit = (match.group(2) or "go").lower()
            return number * UNIT_TO_GB[unit], False

    return np.nan, False
