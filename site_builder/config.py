"""Chemins et réglages de la génération du site statique (aucune fonction ici)."""
from pathlib import Path

# Racine du projet (dossier qui contient site/, docs/, esim/…).
ROOT = Path(__file__).resolve().parent.parent

# Sources du site : gabarit HTML, feuille de styles et scripts (un fichier par fonction).
SITE_DIR = ROOT / "site"
TEMPLATE = SITE_DIR / "index.html"
STYLES = SITE_DIR / "styles.css"
JS_DIR = SITE_DIR / "js"

# Ordre d'assemblage des scripts : données et constantes d'abord, état, puis toutes les
# fonctions (dossier fonctions/, ordre alphabétique), enfin le démarrage de la page.
JS_HEAD = ["donnees.js", "config.js", "etat.js"]
JS_FUNCTIONS_DIR = JS_DIR / "fonctions"
JS_TAIL = ["main.js"]

# Résultat publié par GitHub Pages : la page et l'API statique en lecture seule.
DOCS_DIR = ROOT / "docs"
OUTPUT = DOCS_DIR / "index.html"
API_DIR = DOCS_DIR / "api"

# Adresse du dépôt GitHub, par exemple "https://github.com/<pseudo>/dashboard-esim".
# Si elle est renseignée, un lien « code source » apparaît en pied de page.
REPO_URL = ""

# Description de l'API statique, écrite dans docs/api/index.json.
API_ROUTES = {
    "offers.json": "toutes les offres : {total, offers: [...]}",
    "offers.csv": "toutes les offres au format CSV",
    "stats.json": "les 6 statistiques + KPIs bonus",
    "providers.json": "répartition par fournisseur avec prix moyen au Go",
}
API_NOTE = ("Pour importer, filtrer côté serveur ou écrire, utiliser l'API dynamique api.py "
            "(FastAPI).")
