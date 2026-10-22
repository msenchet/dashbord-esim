"""Moteur de nettoyage et de statistiques des offres eSIM.

Chaque fonction vit dans son propre fichier ; ce module les rassemble pour pouvoir écrire
simplement ``from esim import load_offers, compute_stats``.

Fichiers du paquet :
    config.py                  constantes (chemins, seuils, alias de colonnes…)
    parse_price.py             prix écrit librement → nombre
    parse_data_gb.py           volume de data → Go + détection de l'illimité
    provider_from_filename.py  nom de fichier → nom de fournisseur
    normalize_column.py        nom de colonne importé → nom interne
    read_csv_any_separator.py  lecture d'un CSV séparé par « , » ou « ; »
    records_from_json.py       JSON importé → tableau d'offres
    read_any.py                fichier importé (CSV ou JSON) → tableau brut
    prepare_frame.py           harmonisation des colonnes d'une source
    text_column.py             colonne texte nettoyée
    clean_volume.py            colonnes de volume (Go, illimité, libellé)
    fill_text_fields.py        textes, valeurs par défaut et SKU générés
    clean_offers.py            nettoyage complet
    load_offers.py             chargement des CSV d'origine
    to_records.py              offres → format JSON de l'API
    compute_stats.py           indicateurs globaux
    provider_breakdown.py      répartition par fournisseur
    json_safe.py               valeur numpy → valeur JSON
    print_report.py            rapport texte dans le terminal
"""
from .clean_offers import clean_offers
from .compute_stats import compute_stats
from .config import DATA_DIR, EXPENSIVE_THRESHOLD, EXPORT_COLUMNS
from .json_safe import json_safe
from .load_offers import load_offers
from .parse_data_gb import parse_data_gb
from .parse_price import parse_price
from .prepare_frame import prepare_frame
from .print_report import print_report
from .provider_breakdown import provider_breakdown
from .read_any import read_any
from .records_from_json import records_from_json
from .to_records import to_records

# Noms rendus disponibles par « from esim import * ».
__all__ = [
    "DATA_DIR", "EXPENSIVE_THRESHOLD", "EXPORT_COLUMNS", "clean_offers", "compute_stats",
    "json_safe", "load_offers", "parse_data_gb", "parse_price", "prepare_frame", "print_report",
    "provider_breakdown", "read_any", "records_from_json", "to_records",
]
