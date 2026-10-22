"""Nettoyage des colonnes liées au volume de data (Go, illimité, libellé)."""
import numpy as np
import pandas as pd

from .config import TRUE_WORDS, UNKNOWN_VOLUME, UNLIMITED_LABEL
from .parse_data_gb import parse_data_gb
from .text_column import text_column


def clean_volume(offers: pd.DataFrame) -> None:
    """Remplit data_gb, is_unlimited et data_display (modifie ``offers`` sur place).

    Args:
        offers: tableau des offres en cours de nettoyage.
    """
    # display : libellé du volume fourni par la source (« 3 Go », « Illimité »…).
    display = text_column(offers, "data_display")
    # gb_raw : colonne numérique data_gb brute, ou colonne vide si la source n'en a pas.
    gb_raw = (offers["data_gb"] if "data_gb" in offers.columns
              else pd.Series(np.nan, index=offers.index))
    # parsed : un couple (volume_en_go, est_illimite) par offre.
    parsed = [parse_data_gb(gb, None if pd.isna(disp) else disp)
              for gb, disp in zip(gb_raw, display)]
    offers["data_gb"] = [gb for gb, _ in parsed]
    # flagged : offres marquées illimitées par une colonne « is_unlimited » explicite.
    flagged = text_column(offers, "is_unlimited").str.lower().isin(TRUE_WORDS).fillna(False)
    offers["is_unlimited"] = [unl for _, unl in parsed] | flagged.to_numpy(dtype=bool)
    offers.loc[offers["is_unlimited"], "data_gb"] = np.nan
    # auto_display : libellé reconstruit à partir du volume quand la source n'en donne pas.
    auto_display = pd.Series(
        [f"{gb:g} Go" if pd.notna(gb) else UNKNOWN_VOLUME for gb in offers["data_gb"]],
        index=offers.index)
    offers["data_display"] = display.fillna(auto_display)
    offers.loc[offers["is_unlimited"], "data_display"] = UNLIMITED_LABEL
