"""Lecture d'un fichier importé, CSV ou JSON."""
import io
import json

import pandas as pd

from .read_csv_any_separator import read_csv_any_separator
from .records_from_json import records_from_json


def read_any(content: bytes, filename: str) -> pd.DataFrame:
    """Lit le contenu brut d'un fichier importé, en CSV ou en JSON.

    Le JSON est reconnu à l'extension « .json » ou à un premier caractère « [ » ou « { ».

    Args:
        content: octets du fichier (envoi de formulaire, réponse d'API…).
        filename: nom du fichier, utilisé pour reconnaître le format.

    Returns:
        Le tableau brut des offres.
    """
    # text : le contenu décodé en UTF-8, sans l'éventuel BOM de début de fichier.
    text = content.decode("utf-8-sig", errors="replace")
    if filename.lower().endswith(".json") or text.lstrip()[:1] in "[{":
        return records_from_json(json.loads(text))
    return read_csv_any_separator(io.StringIO(text))
