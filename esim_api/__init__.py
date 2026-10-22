"""API REST des offres eSIM (FastAPI) : import et export des données.

Fichiers du paquet :
    config.py          réglages (CORS, limites, types de paramètres)
    store.py           données gardées en mémoire (origine + imports)
    models.py          structures échangées (filtres, corps de requête)
    app.py             création de l'application et déclaration des routes
    get_filters.py     lecture des filtres dans l'URL
    apply_filters.py   application des filtres aux offres
    merge_offers.py    fusion d'un import dans les données
    reset_offers.py    retour aux données d'origine
    require_key.py     contrôle de la clé API
    parse_import.py    nettoyage des données importées
    root.py, get_*.py, import_*.py, reset_import.py   une route par fichier
"""
from .app import app

# Nom rendu disponible par « from esim_api import * ».
__all__ = ["app"]
