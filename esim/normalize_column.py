"""Normalisation d'un nom de colonne importé."""
import re
import unicodedata

from .config import COLUMN_ALIASES


def normalize_column(name) -> str:
    """Normalise un nom de colonne et applique les alias : « Validité (jours) » → validity_days.

    Étapes : suppression des accents, minuscules, caractères spéciaux remplacés par « _ »,
    puis traduction éventuelle par ``COLUMN_ALIASES``.

    Args:
        name: nom de colonne tel qu'il apparaît dans le fichier importé.

    Returns:
        Le nom interne de la colonne.
    """
    # text : le nom sans accents (é → e), en minuscules, avec « _ » comme seul séparateur.
    text = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "_", text.strip().lower()).strip("_")
    return COLUMN_ALIASES.get(text, text)
