"""Assemblage de l'API REST : création de l'application et déclaration des routes.

Lancer :  uvicorn api:app --reload   puis ouvrir http://localhost:8000/docs

Variables d'environnement :
    ESIM_API_KEY      clé exigée (en-tête X-API-Key) par les routes d'écriture (POST/DELETE) ;
                      sans elle, l'écriture est refusée
    ESIM_OPEN_WRITE   « 1 » = écriture sans clé, pour le développement local uniquement
    ESIM_ALLOW_PRIVATE_URLS  « 1 » = import d'URL locales (localhost…), en local uniquement
    ESIM_CORS      origines autorisées, séparées par des virgules (défaut : *)

Ce fichier ne définit aucune fonction : chaque route vit dans son propre fichier.
"""
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import API_DESCRIPTION, API_TITLE, API_VERSION, CORS_ORIGINS
from .get_offers import get_offers
from .get_offers_csv import get_offers_csv
from .get_providers import get_providers
from .get_sources import get_sources
from .get_stats import get_stats
from .import_file import import_file
from .import_json import import_json
from .import_url import import_url
from .require_key import require_key
from .reset_import import reset_import
from .root import root

# app : l'application FastAPI servie par uvicorn.
app = FastAPI(title=API_TITLE, version=API_VERSION, description=API_DESCRIPTION)

# CORS : autorise les pages web (dont le dashboard GitHub Pages) à appeler l'API.
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS,
                   allow_methods=["*"], allow_headers=["*"])

# protected : dépendance ajoutée aux routes d'écriture (contrôle de la clé API).
protected = [Depends(require_key)]

# ---------- Export (lecture) ----------
app.add_api_route("/", root, methods=["GET"], include_in_schema=False)
app.add_api_route("/api/offers", get_offers, methods=["GET"],
                  summary="Liste des offres (JSON, filtrable et paginée)")
app.add_api_route("/api/offers.csv", get_offers_csv, methods=["GET"],
                  summary="Export CSV des offres filtrées")
app.add_api_route("/api/stats", get_stats, methods=["GET"],
                  summary="Les 6 statistiques + KPIs bonus")
app.add_api_route("/api/providers", get_providers, methods=["GET"],
                  summary="Répartition par fournisseur (+ €/Go)")
app.add_api_route("/api/sources", get_sources, methods=["GET"],
                  summary="Sources de données actuellement chargées")

# ---------- Import (écriture, protégé par la clé API si elle est définie) ----------
app.add_api_route("/api/import/file", import_file, methods=["POST"], dependencies=protected,
                  summary="Importer un ou plusieurs fichiers CSV/JSON")
app.add_api_route("/api/import/json", import_json, methods=["POST"], dependencies=protected,
                  summary="Importer des offres envoyées en JSON")
app.add_api_route("/api/import/url", import_url, methods=["POST"], dependencies=protected,
                  summary="Importer depuis une URL (API JSON ou fichier CSV en ligne)")
app.add_api_route("/api/import", reset_import, methods=["DELETE"], dependencies=protected,
                  summary="Revenir aux données d'origine")
