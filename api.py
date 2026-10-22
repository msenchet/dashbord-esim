"""API REST des offres eSIM (import + export).

Lancer :  uvicorn api:app --reload        puis ouvrir http://localhost:8000/docs

Variables d'environnement :
  ESIM_API_KEY   si définie, les routes d'écriture (POST/DELETE) exigent l'en-tête X-API-Key
  ESIM_CORS      origines autorisées, séparées par des virgules (défaut : *)
"""
from __future__ import annotations

import os
import threading
from typing import Literal

import httpx
import numpy as np
import pandas as pd
from fastapi import Body, Depends, FastAPI, File, Header, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, HttpUrl

from esim_data import (EXPENSIVE_THRESHOLD, EXPORT_COLUMNS, clean_offers, compute_stats, load_offers, prepare_frame,
                       provider_breakdown, read_any, records_from_json, to_records)

MAX_IMPORT_BYTES = 20 * 1024 * 1024
Mode = Literal["append", "replace"]

app = FastAPI(title="API eSIM", version="1.0",
              description="Import (fichier CSV/JSON, JSON brut, URL) et export (JSON/CSV) des offres eSIM.")
app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("ESIM_CORS", "*").split(","),
                   allow_methods=["*"], allow_headers=["*"])


class Store:
    """Jeu de données en mémoire : données d'origine + imports successifs."""

    def __init__(self):
        self.lock = threading.Lock()
        self.base = load_offers()
        self.offers = self.base
        self.sources = ["donnees-test-mybestsim (origine)"]

    def merge(self, new: pd.DataFrame, mode: Mode, label: str) -> dict:
        with self.lock:
            before = 0 if mode == "replace" else len(self.offers)
            combined = new if mode == "replace" else pd.concat([self.offers, new], ignore_index=True)
            # Un SKU déjà présent est mis à jour par la version importée.
            self.offers = combined.drop_duplicates(subset=["sku"], keep="last").reset_index(drop=True)
            self.sources = ([] if mode == "replace" else self.sources) + [label]
            return {"imported_rows": len(new), "total_offers": len(self.offers),
                    "added": len(self.offers) - before, "updated": before + len(new) - len(self.offers),
                    "mode": mode, "sources": self.sources}

    def reset(self):
        with self.lock:
            self.offers, self.sources = self.base, ["donnees-test-mybestsim (origine)"]


store = Store()


def require_key(x_api_key: str | None = Header(default=None)):
    expected = os.environ.get("ESIM_API_KEY")
    if expected and x_api_key != expected:
        raise HTTPException(401, "Clé API invalide ou manquante (en-tête X-API-Key)")


def parse_import(frames: list[tuple[pd.DataFrame, str]]) -> pd.DataFrame:
    try:
        cleaned = clean_offers(pd.concat([prepare_frame(df, name) for df, name in frames], ignore_index=True))
    except (ValueError, KeyError) as exc:
        raise HTTPException(422, f"Données illisibles : {exc}") from exc
    if cleaned.empty:
        raise HTTPException(422, "Aucune offre valide (prix manquant ou illisible sur toutes les lignes)")
    return cleaned


# ---------- Filtres communs aux routes d'export ----------
class Filters:
    def __init__(self,
                 provider: list[str] | None = Query(None, description="Un ou plusieurs fournisseurs"),
                 country: list[str] | None = Query(None, description="Une ou plusieurs destinations"),
                 validity: list[int] | None = Query(None, description="Durées en jours (7, 15, 30…)"),
                 network: list[str] | None = Query(None, description="4G, 5G"),
                 kind: Literal["all", "limited", "unlimited"] = "all",
                 min_price: float | None = None, max_price: float | None = None,
                 q: str | None = Query(None, description="Recherche texte")):
        self.provider, self.country, self.validity, self.network = provider, country, validity, network
        self.kind, self.min_price, self.max_price, self.q = kind, min_price, max_price, q

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        mask = pd.Series(True, index=df.index)
        lower = lambda values: [v.lower() for v in values]
        if self.provider:
            mask &= df["provider"].str.lower().isin(lower(self.provider))
        if self.country:
            mask &= df["country_name"].str.lower().isin(lower(self.country)) | \
                    df["country_code"].fillna("").str.lower().isin(lower(self.country))
        if self.validity:
            mask &= df["validity_days"].isin(self.validity)
        if self.network:
            mask &= df["network"].str.lower().isin(lower(self.network))
        if self.kind != "all":
            mask &= df["is_unlimited"] == (self.kind == "unlimited")
        if self.min_price is not None:
            mask &= df["price"] >= self.min_price
        if self.max_price is not None:
            mask &= df["price"] <= self.max_price
        if self.q:
            haystack = df["provider"] + " " + df["product_name"] + " " + df["country_name"] + " " + df["network"]
            mask &= haystack.str.contains(self.q, case=False, regex=False)
        return df[mask.fillna(False)]


def json_safe(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return None if np.isnan(value) else round(float(value), 4)
    return value


# ---------- Export ----------
@app.get("/", include_in_schema=False)
def root():
    return {"api": "eSIM", "docs": "/docs", "offres": len(store.offers), "sources": store.sources}


@app.get("/api/offers", summary="Liste des offres (JSON, filtrable et paginée)")
def get_offers(f: Filters = Depends(), limit: int = Query(1000, ge=1, le=10000), offset: int = Query(0, ge=0),
               sort: Literal["price", "price_per_gb", "provider", "validity_days", "data_gb"] = "price",
               order: Literal["asc", "desc"] = "asc"):
    df = f.apply(store.offers).sort_values(sort, ascending=order == "asc", na_position="last")
    return {"total": len(df), "limit": limit, "offset": offset,
            "offers": to_records(df.iloc[offset:offset + limit])}


@app.get("/api/offers.csv", summary="Export CSV des offres filtrées")
def get_offers_csv(f: Filters = Depends()):
    df = f.apply(store.offers).sort_values("price")
    csv = pd.DataFrame(to_records(df), columns=EXPORT_COLUMNS).to_csv(index=False)
    return Response("﻿" + csv, media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": 'attachment; filename="offres_esim.csv"'})


@app.get("/api/stats", summary="Les 6 statistiques + KPIs bonus")
def get_stats(f: Filters = Depends()):
    df = f.apply(store.offers)
    if df.empty:
        return {"total_offers": 0}
    stats = {k: json_safe(v) for k, v in compute_stats(df).items()}
    return stats | {"expensive_threshold": EXPENSIVE_THRESHOLD}


@app.get("/api/providers", summary="Répartition par fournisseur (+ €/Go)")
def get_providers(f: Filters = Depends()):
    df = f.apply(store.offers)
    if df.empty:
        return []
    table = provider_breakdown(df).reset_index()
    return [{k: json_safe(v) for k, v in row.items()} for row in table.to_dict(orient="records")]


@app.get("/api/sources", summary="Sources de données actuellement chargées")
def get_sources():
    return {"total_offers": len(store.offers), "sources": store.sources}


# ---------- Import ----------
@app.post("/api/import/file", summary="Importer un ou plusieurs fichiers CSV/JSON", dependencies=[Depends(require_key)])
async def import_file(files: list[UploadFile] = File(...), mode: Mode = "append"):
    frames = []
    for upload in files:
        content = await upload.read()
        if len(content) > MAX_IMPORT_BYTES:
            raise HTTPException(413, f"{upload.filename} dépasse 20 Mo")
        try:
            frames.append((read_any(content, upload.filename or "import.csv"), upload.filename or "import.csv"))
        except Exception as exc:
            raise HTTPException(422, f"{upload.filename} : fichier illisible ({exc})") from exc
    return store.merge(parse_import(frames), mode, ", ".join(name for _, name in frames))


@app.post("/api/import/json", summary="Importer des offres envoyées en JSON", dependencies=[Depends(require_key)])
def import_json(payload: list[dict] | dict = Body(..., examples=[{"offers": [
        {"provider": "MonOpérateur", "country_name": "Japon", "data_gb": 10, "validity_days": 15, "price": 19.9}]}]),
        mode: Mode = "append", source: str = "import-json"):
    try:
        df = records_from_json(payload)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return store.merge(parse_import([(df, source)]), mode, source)


class UrlImport(BaseModel):
    url: HttpUrl
    mode: Mode = "append"


@app.post("/api/import/url", summary="Importer depuis une URL (API JSON ou fichier CSV en ligne)",
          dependencies=[Depends(require_key)])
def import_url(body: UrlImport):
    try:
        resp = httpx.get(str(body.url), timeout=20, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(502, f"Impossible de récupérer {body.url} : {exc}") from exc
    if len(resp.content) > MAX_IMPORT_BYTES:
        raise HTTPException(413, "Réponse supérieure à 20 Mo")
    name = body.url.path.rsplit("/", 1)[-1] if body.url.path else body.url.host
    if "json" in resp.headers.get("content-type", "") and not name.endswith(".json"):
        name += ".json"
    try:
        df = read_any(resp.content, name or "import")
    except Exception as exc:
        raise HTTPException(422, f"Contenu illisible : {exc}") from exc
    return store.merge(parse_import([(df, name or str(body.url))]), body.mode, str(body.url))


@app.delete("/api/import", summary="Revenir aux données d'origine", dependencies=[Depends(require_key)])
def reset_import():
    store.reset()
    return get_sources()
