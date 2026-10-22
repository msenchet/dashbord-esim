"""Nettoyage complet d'offres brutes, quelle que soit leur source."""
import pandas as pd

from .clean_volume import clean_volume
from .config import OBJECT_FIELDS, TRUE_WORDS
from .fill_text_fields import fill_text_fields
from .parse_price import parse_price
from .text_column import text_column


def clean_offers(offers: pd.DataFrame) -> pd.DataFrame:
    """Convertit des offres brutes (déjà passées par prepare_frame) en tableau propre et typé.

    Étapes : prix en nombre, volume et illimité, validité en jours, recharge en booléen,
    textes complétés, puis suppression des offres sans prix et des SKU en double
    (la dernière version d'un SKU l'emporte).

    Args:
        offers: offres brutes, toutes sources confondues.

    Returns:
        Le tableau nettoyé, index remis à zéro.

    Raises:
        ValueError: si aucune colonne de prix n'existe.
    """
    if "price" not in offers.columns:
        raise ValueError("Colonne de prix introuvable (attendu : price ou prix)")
    offers = offers.reset_index(drop=True).copy()

    offers["price"] = offers["price"].map(parse_price)
    clean_volume(offers)
    # Validité : premier nombre trouvé (« 30 jours » → 30), entier pouvant être manquant.
    validity_digits = text_column(offers, "validity_days").str.extract(r"(\d+)")[0]
    offers["validity_days"] = pd.to_numeric(validity_digits, errors="coerce").astype("Int64")
    offers["top_up"] = (text_column(offers, "top_up").str.lower()
                        .isin(TRUE_WORDS).fillna(False).astype(bool))
    # Prix au Go : NaN pour l'illimité et pour un volume nul ou inconnu.
    offers["price_per_gb"] = offers["price"] / offers["data_gb"].where(offers["data_gb"] > 0)
    fill_text_fields(offers)

    offers = offers.dropna(subset=["price"]).drop_duplicates(subset=["sku"], keep="last")
    for col in OBJECT_FIELDS:
        offers[col] = offers[col].astype(object).where(offers[col].notna(), None)
    return offers.reset_index(drop=True)
