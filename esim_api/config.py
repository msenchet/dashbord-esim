"""Réglages de l'API REST (aucune fonction ici)."""
import os
from typing import Literal

# Titre et description affichés dans la documentation interactive (/docs).
API_TITLE = "API eSIM"
API_VERSION = "1.0"
API_DESCRIPTION = ("Import (fichier CSV/JSON, JSON brut, URL) et export (JSON/CSV) "
                   "des offres eSIM.")

# Origines autorisées à appeler l'API depuis un navigateur (CORS), séparées par des virgules.
# « * » = toutes, ce qui permet au dashboard GitHub Pages de lire l'API.
CORS_ORIGINS = os.environ.get("ESIM_CORS", "*").split(",")

# Nom de la variable d'environnement contenant la clé API (routes d'écriture protégées).
API_KEY_ENV = "ESIM_API_KEY"

# Variable d'environnement qui ouvre les routes d'écriture sans clé (« 1 » = ouvert).
# Réservée au développement sur son ordinateur : sans clé, n'importe quel site web visité
# pourrait remplacer les données, car le CORS autorise toutes les origines.
OPEN_WRITE_ENV = "ESIM_OPEN_WRITE"

# Nombre maximal de fichiers par import et d'offres gardées en mémoire (protège la mémoire
# du serveur contre des imports répétés ou démesurés).
MAX_FILES = 20
MAX_OFFERS = 200_000

# Délai maximal (secondes) pour télécharger une URL lors d'un import.
URL_TIMEOUT_SECONDS = 20

# Libellé de la source chargée au démarrage.
ORIGIN_LABEL = "donnees-test-mybestsim (origine)"

# Nombre d'offres renvoyées par défaut et au maximum par /api/offers.
DEFAULT_LIMIT = 1000
MAX_LIMIT = 10000

# Mode d'import : « append » ajoute (un SKU existant est mis à jour), « replace » remplace tout.
Mode = Literal["append", "replace"]

# Type de forfait filtré : tous, à volume limité ou illimités.
Kind = Literal["all", "limited", "unlimited"]

# Colonnes autorisées pour le tri de /api/offers, et sens du tri.
SortKey = Literal["price", "price_per_gb", "provider", "validity_days", "data_gb"]
SortOrder = Literal["asc", "desc"]
