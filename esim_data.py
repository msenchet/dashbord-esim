"""Moteur de nettoyage et de statistiques pour les offres eSIM.

Usage en ligne de commande :  python esim_data.py [dossier_csv]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent / "donnees-test-mybestsim"
EXPENSIVE_THRESHOLD = 100.0  # €

UNLIMITED_WORDS = re.compile(r"illimit|unlimited|∞", re.IGNORECASE)
VOLUME_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(to|tb|go|gb|mo|mb)?", re.IGNORECASE)
UNIT_TO_GB = {"to": 1000, "tb": 1000, "go": 1, "gb": 1, "mo": 1 / 1000, "mb": 1 / 1000}


def parse_price(value) -> float:
    """'12,45 €', '€12.45', '1 234,50' ou 12.45 -> 12.45 (NaN si illisible)."""
    if pd.isna(value):
        return np.nan
    text = str(value).replace(" ", "").replace(" ", "")
    text = re.sub(r"[^\d,.\-]", "", text)
    if "," in text and "." in text:
        # Le dernier séparateur rencontré est le séparateur décimal.
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    else:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return np.nan


def parse_data_gb(gb_value, display_value=None) -> tuple[float, bool]:
    """Renvoie (volume en Go, est_illimité). Les forfaits illimités ont un volume NaN."""
    for raw in (display_value, gb_value):
        if isinstance(raw, str) and UNLIMITED_WORDS.search(raw):
            return np.nan, True

    # Colonne numérique data_gb en priorité, sinon le libellé ("500 Mo", "3 Go").
    if not pd.isna(gb_value) and str(gb_value).strip():
        number = parse_price(gb_value)
        unit_match = VOLUME_RE.search(str(gb_value))
        unit = (unit_match.group(2) or "go").lower() if unit_match else "go"
        if not np.isnan(number):
            return number * UNIT_TO_GB[unit], False

    if isinstance(display_value, str):
        match = VOLUME_RE.search(display_value)
        if match:
            number = float(match.group(1).replace(",", "."))
            unit = (match.group(2) or "go").lower()
            return number * UNIT_TO_GB[unit], False

    return np.nan, False


def provider_from_filename(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip().title()


def read_csv_any_separator(path: Path) -> pd.DataFrame:
    # sep=None laisse pandas détecter , ou ; automatiquement.
    return pd.read_csv(path, sep=None, engine="python", dtype=str,
                       encoding="utf-8-sig", skip_blank_lines=True)


def load_offers(folder: Path | str = DATA_DIR) -> pd.DataFrame:
    """Lit tous les CSV du dossier et renvoie un DataFrame propre et typé."""
    folder = Path(folder)
    frames = []
    for path in sorted(folder.glob("*.csv")):
        df = read_csv_any_separator(path)
        df.columns = [c.strip().lower() for c in df.columns]
        if "provider" not in df.columns or df["provider"].isna().all():
            df["provider"] = provider_from_filename(path)
        df["provider"] = df["provider"].fillna(provider_from_filename(path)).str.strip()
        df["source_file"] = path.name
        frames.append(df)

    if not frames:
        raise FileNotFoundError(f"Aucun fichier .csv trouvé dans {folder}")

    offers = pd.concat(frames, ignore_index=True)

    offers["price"] = offers["price"].map(parse_price)
    parsed = [parse_data_gb(gb, disp) for gb, disp in
              zip(offers.get("data_gb"), offers.get("data_display", pd.Series(index=offers.index)))]
    offers["data_gb"] = [gb for gb, _ in parsed]
    offers["is_unlimited"] = [unl for _, unl in parsed]
    offers["validity_days"] = pd.to_numeric(offers["validity_days"].str.extract(r"(\d+)")[0],
                                            errors="coerce").astype("Int64")
    offers["top_up"] = offers["top_up"].str.strip().str.lower().isin(["oui", "yes", "true", "1"])
    offers["price_per_gb"] = offers["price"] / offers["data_gb"]  # NaN pour l'illimité

    for col in ["product_name", "country_code", "country_name", "network", "currency"]:
        if col in offers.columns:
            offers[col] = offers[col].str.strip()

    offers = offers.dropna(subset=["price"]).drop_duplicates(subset=["sku"] if "sku" in offers else None)
    return offers.reset_index(drop=True)


def compute_stats(offers: pd.DataFrame) -> dict:
    """Les 6 statistiques demandées + KPIs bonus."""
    limited = offers[~offers["is_unlimited"]]
    return {
        "total_offers": len(offers),
        "offers_over_100": int((offers["price"] > EXPENSIVE_THRESHOLD).sum()),
        "price_min": offers["price"].min(),
        "price_max": offers["price"].max(),
        "price_mean": offers["price"].mean(),
        # Moyenne calculée uniquement sur les forfaits à volume fini.
        "data_mean_gb": limited["data_gb"].mean(),
        "unlimited_offers": int(offers["is_unlimited"].sum()),
        "providers": offers["provider"].nunique(),
        "price_per_gb_mean": limited["price_per_gb"].mean(),
    }


def provider_breakdown(offers: pd.DataFrame) -> pd.DataFrame:
    """Répartition par fournisseur + prix moyen au Go (€/Go, hors illimité)."""
    grouped = offers.groupby("provider")
    table = pd.DataFrame({
        "offres": grouped.size(),
        "part_%": grouped.size() / len(offers) * 100,
        "prix_moyen": grouped["price"].mean(),
        "prix_min": grouped["price"].min(),
        "prix_max": grouped["price"].max(),
        "offres_illimitees": grouped["is_unlimited"].sum().astype(int),
        "prix_moyen_par_go": grouped["price_per_gb"].mean(),
    })
    return table.sort_values("offres", ascending=False)


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR
    df = load_offers(folder)
    stats = compute_stats(df)
    print("=== Statistiques globales ===")
    print(f"Cartes eSIM         : {stats['total_offers']}")
    print(f"Offres > 100 €      : {stats['offers_over_100']}")
    print(f"Prix min / max / moy: {stats['price_min']:.2f} € / {stats['price_max']:.2f} € / {stats['price_mean']:.2f} €")
    print(f"Data moyenne        : {stats['data_mean_gb']:.2f} Go (hors {stats['unlimited_offers']} illimités)")
    print(f"Prix moyen au Go    : {stats['price_per_gb_mean']:.2f} €/Go")
    print("\n=== Par fournisseur ===")
    print(provider_breakdown(df).round(2).to_string())
