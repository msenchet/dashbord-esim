"""Fusion d'offres importées dans le jeu de données de l'API."""
import pandas as pd

from . import store
from .config import Mode


def merge_offers(new: pd.DataFrame, mode: Mode, label: str) -> dict:
    """Ajoute ou remplace les offres servies par l'API.

    En mode « append », un SKU déjà présent est remplacé par la version importée.

    Args:
        new: offres importées, déjà nettoyées.
        mode: « append » pour ajouter, « replace » pour remplacer toutes les offres.
        label: nom lisible de la source (fichier ou URL), ajouté à la liste des sources.

    Returns:
        Le bilan de l'import : lignes importées, total, ajoutées, mises à jour, sources.
    """
    with store.lock:
        # before : nombre d'offres conservées avant fusion (0 si on remplace tout).
        before = 0 if mode == "replace" else len(store.offers)
        combined = new if mode == "replace" else pd.concat([store.offers, new], ignore_index=True)
        store.offers = (combined.drop_duplicates(subset=["sku"], keep="last")
                        .reset_index(drop=True))
        store.sources = ([] if mode == "replace" else store.sources) + [label]
        return {
            "imported_rows": len(new),
            "total_offers": len(store.offers),
            "added": len(store.offers) - before,
            "updated": before + len(new) - len(store.offers),
            "mode": mode,
            "sources": store.sources,
        }
