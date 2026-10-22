"""Génération du site statique (docs/) publié sur GitHub Pages.

Fichiers du paquet :
    config.py          chemins, ordre des scripts, lien du dépôt
    build_payload.py   offres → format compact injecté dans la page
    bundle_scripts.py  assemblage des fichiers JavaScript de site/js/
    render_html.py     gabarit + styles + scripts + données → HTML final
    write_json.py      écriture d'un fichier JSON
    build_api.py       API statique docs/api/
    build_site.py      génération complète
"""
from .build_site import build_site

# Nom rendu disponible par « from site_builder import * ».
__all__ = ["build_site"]
