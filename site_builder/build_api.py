"""Génération de l'API statique (fichiers JSON et CSV en lecture seule)."""
import pandas as pd

from esim import EXPORT_COLUMNS, compute_stats, json_safe, provider_breakdown, to_records

from .config import API_DIR, API_NOTE, API_ROUTES
from .write_json import write_json


def build_api(offers: pd.DataFrame, generated_at: str) -> None:
    """Écrit docs/api/ : offers.json, offers.csv, stats.json, providers.json et index.json.

    GitHub Pages sert ces fichiers avec CORS ouvert : n'importe quel site peut les lire.

    Args:
        offers: offres nettoyées.
        generated_at: date de génération (ISO 8601), écrite dans chaque fichier JSON.
    """
    API_DIR.mkdir(parents=True, exist_ok=True)
    # stats : indicateurs globaux ; providers : répartition ; records : offres triées par prix.
    stats = {key: json_safe(value) for key, value in compute_stats(offers).items()}
    providers = [{key: json_safe(value) for key, value in row.items()}
                 for row in provider_breakdown(offers).reset_index().to_dict(orient="records")]
    records = to_records(offers.sort_values("price"))

    write_json(API_DIR / "offers.json",
               {"generated_at": generated_at, "total": len(records), "offers": records},
               compact=True)
    write_json(API_DIR / "stats.json", {"generated_at": generated_at, **stats})
    write_json(API_DIR / "providers.json", {"generated_at": generated_at, "providers": providers})
    csv = pd.DataFrame(records, columns=EXPORT_COLUMNS).to_csv(index=False)
    (API_DIR / "offers.csv").write_text("﻿" + csv, encoding="utf-8")
    write_json(API_DIR / "index.json", {
        "name": "API eSIM (statique, lecture seule)",
        "generated_at": generated_at,
        "routes": API_ROUTES,
        "fields": EXPORT_COLUMNS,
        "note": API_NOTE,
    })
