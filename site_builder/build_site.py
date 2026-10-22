"""Génération complète du site statique pour GitHub Pages."""
from datetime import datetime, timezone

from esim import load_offers

from .build_api import build_api
from .config import API_DIR, OUTPUT, ROOT
from .render_html import render_html


def build_site() -> None:
    """Écrit docs/index.html (le dashboard) et docs/api/ (l'API statique), puis affiche un bilan.

    Le fichier docs/.nojekyll empêche GitHub Pages de transformer le contenu de docs/.
    """
    # offers : offres nettoyées ; generated_at : date de génération en temps universel.
    offers = load_offers()
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(render_html(offers), encoding="utf-8")
    (OUTPUT.parent / ".nojekyll").touch()
    build_api(offers, generated_at)
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"{OUTPUT.relative_to(ROOT)} généré ({size_kb:.0f} Ko, {len(offers)} offres)")
    print(f"API statique : {', '.join(sorted(p.name for p in API_DIR.iterdir()))}")
