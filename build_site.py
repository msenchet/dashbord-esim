"""Génère la version statique du dashboard pour GitHub Pages.

  docs/index.html          le dashboard (données nettoyées injectées dans site_template.html)
  docs/api/offers.json     API statique en lecture seule, au même format que api.py
  docs/api/offers.csv
  docs/api/stats.json
  docs/api/providers.json
  docs/api/index.json      description des routes

Usage : python build_site.py
"""
import json
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from esim_data import EXPORT_COLUMNS, compute_stats, load_offers, provider_breakdown, to_records

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "site_template.html"
OUTPUT = ROOT / "docs" / "index.html"
API_DIR = ROOT / "docs" / "api"
# Ex. "https://github.com/<pseudo>/dashboard-esim" : ajoute un lien « code source » en pied de page.
REPO_URL = ""


def build_payload(offers):
    """Format colonnes compact : les fournisseurs et pays sont stockés une seule fois."""
    providers = sorted(offers["provider"].unique())
    countries = sorted(offers["country_name"].unique())
    codes = offers.groupby("country_name")["country_code"].first()
    p_index = {p: i for i, p in enumerate(providers)}
    c_index = {c: i for i, c in enumerate(countries)}
    return {
        "providers": providers,
        "countries": countries,
        "codes": [codes.get(c) for c in countries],
        "sku": offers["sku"].tolist(),
        "provider": offers["provider"].map(p_index).tolist(),
        "country": offers["country_name"].map(c_index).tolist(),
        "name": offers["product_name"].tolist(),
        "gb": [None if unl else round(float(gb), 3) for gb, unl in zip(offers["data_gb"], offers["is_unlimited"])],
        "validity": offers["validity_days"].astype(int).tolist(),
        "price": offers["price"].round(2).tolist(),
        "network": offers["network"].tolist(),
        "top_up": offers["top_up"].astype(int).tolist(),
    }


def json_safe(value):
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return None if np.isnan(value) else round(float(value), 4)
    return value


def write_json(path: Path, data, compact=False):
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":")) if compact else         json.dumps(data, ensure_ascii=False, indent=1)
    path.write_text(text, encoding="utf-8")


def build_api(offers, generated_at: str):
    API_DIR.mkdir(parents=True, exist_ok=True)
    stats = {k: json_safe(v) for k, v in compute_stats(offers).items()}
    providers = [{k: json_safe(v) for k, v in row.items()}
                 for row in provider_breakdown(offers).reset_index().to_dict(orient="records")]
    records = to_records(offers.sort_values("price"))

    write_json(API_DIR / "offers.json", {"generated_at": generated_at, "total": len(records), "offers": records}, compact=True)
    write_json(API_DIR / "stats.json", {"generated_at": generated_at, **stats})
    write_json(API_DIR / "providers.json", {"generated_at": generated_at, "providers": providers})
    (API_DIR / "offers.csv").write_text(
        "﻿" + pd.DataFrame(records, columns=EXPORT_COLUMNS).to_csv(index=False), encoding="utf-8")
    write_json(API_DIR / "index.json", {
        "name": "API eSIM (statique, lecture seule)",
        "generated_at": generated_at,
        "routes": {
            "offers.json": "toutes les offres : {total, offers: [...]}",
            "offers.csv": "toutes les offres au format CSV",
            "stats.json": "les 6 statistiques + KPIs bonus",
            "providers.json": "répartition par fournisseur avec prix moyen au Go",
        },
        "fields": EXPORT_COLUMNS,
        "note": "Pour importer, filtrer côté serveur ou écrire, utiliser l'API dynamique api.py (FastAPI).",
    })


def main():
    offers = load_offers()
    stats = compute_stats(offers)
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
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
    build_api(offers, generated_at)
    print(f"{OUTPUT.relative_to(ROOT)} généré ({OUTPUT.stat().st_size / 1024:.0f} Ko, {len(offers)} offres)")
    print(f"API statique : {', '.join(sorted(p.name for p in API_DIR.iterdir()))}")


if __name__ == "__main__":
    main()
