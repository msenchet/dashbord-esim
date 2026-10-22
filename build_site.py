"""Génère la version statique du dashboard pour GitHub Pages.

    docs/index.html          le dashboard, à partir de site/ (gabarit, styles, scripts)
    docs/api/*.json, *.csv   l'API statique en lecture seule

Usage : python build_site.py
Tout le code se trouve dans le paquet site_builder/ (un fichier par fonction).
"""
from site_builder import build_site

if __name__ == "__main__":
    build_site()
