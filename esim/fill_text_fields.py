"""Nettoyage des colonnes texte et création des valeurs manquantes."""
import pandas as pd

from .config import DEFAULT_COUNTRY, DEFAULT_CURRENCY, DEFAULT_NETWORK, TEXT_FIELDS
from .text_column import text_column


def fill_text_fields(offers: pd.DataFrame) -> None:
    """Nettoie les textes et complète destination, réseau, devise, nom d'offre et SKU.

    Modifie ``offers`` sur place. Le volume (data_display) et la validité doivent déjà
    être nettoyés, car ils servent à fabriquer le nom d'offre manquant.

    Args:
        offers: tableau des offres en cours de nettoyage.
    """
    for col in TEXT_FIELDS:
        offers[col] = text_column(offers, col)
    offers["country_name"] = offers["country_name"].fillna(DEFAULT_COUNTRY)
    offers["network"] = offers["network"].fillna(DEFAULT_NETWORK)
    offers["currency"] = offers["currency"].fillna(DEFAULT_CURRENCY)

    # validity_txt : « 7 jours » précédé d'un espace, ou texte vide si la validité est inconnue.
    validity_txt = (" " + offers["validity_days"].astype("string") + " jours").fillna("")
    offers["product_name"] = offers["product_name"].fillna(
        "eSIM " + offers["country_name"] + " " + offers["data_display"] + validity_txt)

    # generated : identifiant stable fabriqué pour les offres sans SKU
    # (fournisseur en minuscules + empreinte du nom d'offre et du prix).
    provider_slug = offers["provider"].str.lower().str.replace(r"\W+", "-", regex=True)
    fingerprint = pd.util.hash_pandas_object(offers[["product_name", "price"]], index=False)
    generated = provider_slug + "-" + fingerprint.astype(str)
    offers["sku"] = offers["sku"].fillna(generated)
