"""Chargement des fichiers CSV d'origine."""
from pathlib import Path

import pandas as pd

from .clean_offers import clean_offers
from .config import DATA_DIR
from .prepare_frame import prepare_frame
from .read_csv_any_separator import read_csv_any_separator


def load_offers(folder: Path | str = DATA_DIR) -> pd.DataFrame:
    """Lit tous les fichiers .csv d'un dossier et renvoie les offres nettoyées.

    Args:
        folder: dossier à parcourir (par défaut, les données d'origine du projet).

    Returns:
        Le tableau propre de toutes les offres.

    Raises:
        FileNotFoundError: si le dossier ne contient aucun fichier CSV.
    """
    folder = Path(folder)
    # frames : un tableau harmonisé par fichier CSV, dans l'ordre alphabétique des fichiers.
    frames = [prepare_frame(read_csv_any_separator(path), path.name)
              for path in sorted(folder.glob("*.csv"))]
    if not frames:
        raise FileNotFoundError(f"Aucun fichier .csv trouvé dans {folder}")
    return clean_offers(pd.concat(frames, ignore_index=True))
