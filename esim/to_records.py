"""Conversion des offres au format JSON de l'API."""
import pandas as pd

from .config import EXPORT_COLUMNS


def to_records(offers: pd.DataFrame) -> list[dict]:
    """Transforme les offres en liste de dictionnaires prêts pour le JSON (NaN → null).

    Les prix et volumes sont arrondis (3 décimales, 4 pour le prix au Go), la validité
    devient un entier et les indicateurs deviennent de vrais booléens.

    Args:
        offers: tableau nettoyé des offres.

    Returns:
        Une liste d'offres, chacune avec les colonnes de ``EXPORT_COLUMNS``.
    """
    # table : colonnes exportées converties en objets Python, valeurs manquantes → None.
    table = offers[EXPORT_COLUMNS].astype(object)
    table = table.where(pd.notna(table), None)
    records = table.to_dict(orient="records")
    for record in records:
        for key in ("price", "data_gb", "price_per_gb"):
            if record[key] is not None:
                record[key] = round(float(record[key]), 4 if key == "price_per_gb" else 3)
        validity = record["validity_days"]
        record["validity_days"] = None if validity is None else int(validity)
        record["is_unlimited"] = bool(record["is_unlimited"])
        record["top_up"] = bool(record["top_up"])
    return records
