"""Moteur de nettoyage et de statistiques pour les offres eSIM.

Usage en ligne de commande :  python esim_data.py [dossier_csv]
"""
from __future__ import annotations

import io
import json
import re
import sys
import unicodedata
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


# Noms de colonnes acceptés à l'import -> nom interne
COLUMN_ALIASES = {
    "fournisseur": "provider", "operateur": "provider",
    "offre": "product_name", "nom": "product_name", "name": "product_name",
    "pays": "country_name", "destination": "country_name", "country": "country_name",
    "data": "data_display", "volume": "data_display",
    "data_go": "data_gb", "go": "data_gb",
    "validite": "validity_days", "validite_jours": "validity_days", "validity": "validity_days", "duree": "validity_days",
    "prix": "price", "prix_eur": "price",
    "reseau": "network", "recharge": "top_up", "devise": "currency", "illimite": "is_unlimited",
}
TRUE_WORDS = ["oui", "yes", "true", "1", "vrai"]
EXPORT_COLUMNS = ["sku", "provider", "product_name", "country_code", "country_name", "data_gb", "data_display",
                  "is_unlimited", "validity_days", "price", "currency", "price_per_gb", "network", "top_up"]


def normalize_column(name) -> str:
    """'Validité (jours)' -> 'validite_jours', puis application des alias."""
    text = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "_", text.strip().lower()).strip("_")
    return COLUMN_ALIASES.get(text, text)


def read_csv_any_separator(source) -> pd.DataFrame:
    """Lit un chemin ou un flux CSV ; sep=None laisse pandas détecter , ou ; automatiquement."""
    return pd.read_csv(source, sep=None, engine="python", dtype=str,
                       encoding="utf-8-sig", skip_blank_lines=True)


def records_from_json(payload) -> pd.DataFrame:
    """Accepte une liste d'offres, {"offers": [...]} (format de l'API) ou {"data": [...]}."""
    if isinstance(payload, dict):
        payload = payload.get("offers", payload.get("data", payload.get("items")))
    if not isinstance(payload, list):
        raise ValueError("JSON attendu : une liste d'offres ou un objet {\"offers\": [...]}")
    return pd.DataFrame(payload)


def read_any(content: bytes, filename: str) -> pd.DataFrame:
    """Lit un fichier importé (CSV ou JSON) à partir de son contenu brut."""
    text = content.decode("utf-8-sig", errors="replace")
    if filename.lower().endswith(".json") or text.lstrip()[:1] in "[{":
        return records_from_json(json.loads(text))
    return read_csv_any_separator(io.StringIO(text))


def prepare_frame(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """Harmonise les colonnes d'une source et complète le fournisseur depuis le nom de fichier."""
    df = df.copy()
    df.columns = [normalize_column(c) for c in df.columns]
    df = df.loc[:, ~df.columns.duplicated()]
    fallback = provider_from_filename(Path(source_name))
    if "provider" not in df.columns:
        df["provider"] = fallback
    df["provider"] = df["provider"].astype("string").str.strip().replace("", pd.NA).fillna(fallback)
    df["source_file"] = source_name
    return df


def text_column(offers: pd.DataFrame, col: str) -> pd.Series:
    if col not in offers.columns:
        return pd.Series(pd.NA, index=offers.index, dtype="string")
    return offers[col].astype("string").str.strip().replace("", pd.NA)


def clean_offers(offers: pd.DataFrame) -> pd.DataFrame:
    """Convertit des offres brutes (toutes sources confondues) en DataFrame propre et typé."""
    if "price" not in offers.columns:
        raise ValueError("Colonne de prix introuvable (attendu : price ou prix)")
    offers = offers.reset_index(drop=True).copy()

    offers["price"] = offers["price"].map(parse_price)
    display = text_column(offers, "data_display")
    gb_raw = offers["data_gb"] if "data_gb" in offers.columns else pd.Series(np.nan, index=offers.index)
    parsed = [parse_data_gb(gb, None if pd.isna(disp) else disp) for gb, disp in zip(gb_raw, display)]
    offers["data_gb"] = [gb for gb, _ in parsed]
    flagged = text_column(offers, "is_unlimited").str.lower().isin(TRUE_WORDS).fillna(False)
    offers["is_unlimited"] = [unl for _, unl in parsed] | flagged.to_numpy(dtype=bool)
    offers.loc[offers["is_unlimited"], "data_gb"] = np.nan
    offers["data_display"] = display.fillna(
        pd.Series([f"{gb:g} Go" if pd.notna(gb) else "N/C" for gb in offers["data_gb"]], index=offers.index))
    offers.loc[offers["is_unlimited"], "data_display"] = "Illimité"

    offers["validity_days"] = pd.to_numeric(text_column(offers, "validity_days").str.extract(r"(\d+)")[0],
                                            errors="coerce").astype("Int64")
    offers["top_up"] = text_column(offers, "top_up").str.lower().isin(TRUE_WORDS).fillna(False).astype(bool)
    offers["price_per_gb"] = offers["price"] / offers["data_gb"].where(offers["data_gb"] > 0)  # NaN pour l'illimité

    for col in ["product_name", "country_code", "country_name", "network", "currency", "sku"]:
        offers[col] = text_column(offers, col)
    offers["country_name"] = offers["country_name"].fillna("Inconnu")
    offers["network"] = offers["network"].fillna("N/C")
    offers["currency"] = offers["currency"].fillna("EUR")
    validity_txt = (" " + offers["validity_days"].astype("string") + " jours").fillna("")
    offers["product_name"] = offers["product_name"].fillna(
        "eSIM " + offers["country_name"] + " " + offers["data_display"] + validity_txt)
    # Offres sans identifiant : on en fabrique un stable (fournisseur + contenu).
    generated = (offers["provider"].str.lower().str.replace(r"\W+", "-", regex=True) + "-"
                 + pd.util.hash_pandas_object(offers[["product_name", "price"]], index=False).astype(str))
    offers["sku"] = offers["sku"].fillna(generated)

    offers = offers.dropna(subset=["price"]).drop_duplicates(subset=["sku"], keep="last")
    for col in ["provider", "product_name", "country_code", "country_name", "data_display",
                "network", "currency", "sku", "source_file"]:
        offers[col] = offers[col].astype(object).where(offers[col].notna(), None)
    return offers.reset_index(drop=True)


def load_offers(folder: Path | str = DATA_DIR) -> pd.DataFrame:
    """Lit tous les CSV du dossier et renvoie un DataFrame propre et typé."""
    folder = Path(folder)
    frames = [prepare_frame(read_csv_any_separator(path), path.name) for path in sorted(folder.glob("*.csv"))]
    if not frames:
        raise FileNotFoundError(f"Aucun fichier .csv trouvé dans {folder}")
    return clean_offers(pd.concat(frames, ignore_index=True))


def to_records(offers: pd.DataFrame) -> list[dict]:
    """Offres au format JSON de l'API (NaN -> null)."""
    out = offers[EXPORT_COLUMNS].astype(object)
    out = out.where(pd.notna(out), None)
    records = out.to_dict(orient="records")
    for r in records:
        for key in ("price", "data_gb", "price_per_gb"):
            if r[key] is not None:
                r[key] = round(float(r[key]), 4 if key == "price_per_gb" else 3)
        r["validity_days"] = None if r["validity_days"] is None else int(r["validity_days"])
        r["is_unlimited"], r["top_up"] = bool(r["is_unlimited"]), bool(r["top_up"])
    return records


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
