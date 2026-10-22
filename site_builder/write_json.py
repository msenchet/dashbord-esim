"""Écriture d'un fichier JSON."""
import json
from pathlib import Path


def write_json(path: Path, data, compact: bool = False) -> None:
    """Écrit des données en JSON UTF-8 (accents conservés).

    Args:
        path: fichier à écrire.
        data: données sérialisables.
        compact: True pour supprimer espaces et retours à la ligne (gros fichiers).
    """
    if compact:
        text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    else:
        text = json.dumps(data, ensure_ascii=False, indent=1)
    path.write_text(text, encoding="utf-8")
