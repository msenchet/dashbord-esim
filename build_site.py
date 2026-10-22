"""Génère la version statique du dashboard pour GitHub Pages : docs/index.html

Usage : python build_site.py
Les données sont nettoyées par esim_data.py puis injectées dans site_template.html.
"""
import json
from datetime import date
from pathlib import Path

from esim_data import compute_stats, load_offers

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "site_template.html"
OUTPUT = ROOT / "docs" / "index.html"
# Ex. "https://github.com/<pseudo>/dashboard-esim" : ajoute un lien « code source » en pied de page.
REPO_URL = ""


def build_payload(offers):
    """Format colonnes compact : les fournisseurs et pays sont stockés une seule fois."""
    providers = sorted(offers["provider"].unique())
    countries = sorted(offers["country_name"].unique())
    p_index = {p: i for i, p in enumerate(providers)}
    c_index = {c: i for i, c in enumerate(countries)}
    return {
        "providers": providers,
        "countries": countries,
        "provider": offers["provider"].map(p_index).tolist(),
        "country": offers["country_name"].map(c_index).tolist(),
        "name": offers["product_name"].tolist(),
        "gb": [None if unl else round(float(gb), 3) for gb, unl in zip(offers["data_gb"], offers["is_unlimited"])],
        "validity": offers["validity_days"].astype(int).tolist(),
        "price": offers["price"].round(2).tolist(),
        "network": offers["network"].tolist(),
        "top_up": offers["top_up"].astype(int).tolist(),
    }


def main():
    offers = load_offers()
    stats = compute_stats(offers)
    payload = json.dumps(build_payload(offers), ensure_ascii=False, separators=(",", ":"))

    html = (TEMPLATE.read_text(encoding="utf-8")
            .replace("__DATA__", payload)
            .replace("__TOTAL__", f"{stats['total_offers']:,}".replace(",", " "))
            .replace("__PROVIDERS__", str(stats["providers"]))
            .replace("__FILES__", str(offers["source_file"].nunique()))
            .replace("__BUILT__", date.today().strftime("%d/%m/%Y"))
            .replace("__REPO_LINK__", f' · <a href="{REPO_URL}">code source</a>' if REPO_URL else ""))

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    (OUTPUT.parent / ".nojekyll").touch()
    print(f"{OUTPUT.relative_to(ROOT)} généré ({OUTPUT.stat().st_size / 1024:.0f} Ko, {len(offers)} offres)")


if __name__ == "__main__":
    main()
