"""Constantes partagées par tout le moteur de nettoyage des offres eSIM.

Ce fichier ne contient aucune fonction : uniquement des réglages, chacun documenté.
"""
import re
from pathlib import Path

# Dossier contenant les 18 fichiers CSV d'origine (un fichier par fournisseur).
DATA_DIR = Path(__file__).resolve().parent.parent / "donnees-test-mybestsim"

# Seuil (en euros) au-delà duquel une offre est comptée comme « chère » (KPI « Offres > 100 € »).
EXPENSIVE_THRESHOLD = 100.0

# Expression qui reconnaît un forfait illimité dans un libellé : « Illimité », « unlimited », « ∞ ».
UNLIMITED_WORDS = re.compile(r"illimit|unlimited|∞", re.IGNORECASE)

# Expression qui extrait un volume et son unité d'un texte : « 500 Mo », « 3,5 Go », « 1 To ».
# Groupe 1 = le nombre, groupe 2 = l'unité (facultative, Go par défaut).
VOLUME_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(to|tb|go|gb|mo|mb)?", re.IGNORECASE)

# Facteur de conversion de chaque unité vers le gigaoctet (Go).
UNIT_TO_GB = {"to": 1000, "tb": 1000, "go": 1, "gb": 1, "mo": 1 / 1000, "mb": 1 / 1000}

# Noms de colonnes acceptés à l'import (déjà normalisés : minuscules, sans accent)
# associés au nom interne utilisé par le moteur.
COLUMN_ALIASES = {
    "fournisseur": "provider",
    "operateur": "provider",
    "offre": "product_name",
    "nom": "product_name",
    "name": "product_name",
    "pays": "country_name",
    "destination": "country_name",
    "country": "country_name",
    "data": "data_display",
    "volume": "data_display",
    "data_go": "data_gb",
    "go": "data_gb",
    "validite": "validity_days",
    "validite_jours": "validity_days",
    "validity": "validity_days",
    "duree": "validity_days",
    "prix": "price",
    "prix_eur": "price",
    "reseau": "network",
    "recharge": "top_up",
    "devise": "currency",
    "illimite": "is_unlimited",
}

# Valeurs texte considérées comme « vrai » (colonnes recharge et illimité).
TRUE_WORDS = ["oui", "yes", "true", "1", "vrai"]

# Colonnes exportées (API, fichiers JSON/CSV), dans cet ordre.
EXPORT_COLUMNS = [
    "sku", "provider", "product_name", "country_code", "country_name", "data_gb",
    "data_display", "is_unlimited", "validity_days", "price", "currency", "price_per_gb",
    "network", "top_up",
]

# Colonnes texte nettoyées (espaces retirés, vides remplacés par une valeur manquante).
TEXT_FIELDS = ["product_name", "country_code", "country_name", "network", "currency", "sku"]

# Colonnes converties en objets Python simples (None au lieu de <NA>) en fin de nettoyage,
# pour que l'export JSON et les comparaisons restent simples.
OBJECT_FIELDS = [
    "provider", "product_name", "country_code", "country_name", "data_display",
    "network", "currency", "sku", "source_file",
]

# Valeurs par défaut quand une colonne est absente ou vide.
DEFAULT_COUNTRY = "Inconnu"   # destination inconnue
DEFAULT_NETWORK = "N/C"       # réseau non communiqué
DEFAULT_CURRENCY = "EUR"      # toutes les offres d'origine sont en euros
UNKNOWN_VOLUME = "N/C"        # libellé d'un volume impossible à lire
UNLIMITED_LABEL = "Illimité"  # libellé affiché pour un forfait illimité
