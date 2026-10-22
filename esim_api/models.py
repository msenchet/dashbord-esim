"""Structures de données échangées par l'API (aucune fonction ici)."""
from dataclasses import dataclass

from pydantic import BaseModel, HttpUrl

from .config import Kind, Mode


class UrlImport(BaseModel):
    """Corps de la requête POST /api/import/url."""

    # url : adresse d'une API JSON ou d'un fichier CSV en ligne à importer.
    url: HttpUrl
    # mode : « append » (ajouter) ou « replace » (remplacer les données).
    mode: Mode = "append"


@dataclass
class OfferFilters:
    """Filtres communs aux routes d'export ; un champ vide (None) ne filtre pas."""

    # provider : fournisseurs retenus (comparaison sans tenir compte des majuscules).
    provider: list[str] | None = None
    # country : destinations retenues, par nom (« Japon ») ou code (« JP »).
    country: list[str] | None = None
    # validity : durées de validité retenues, en jours.
    validity: list[int] | None = None
    # network : réseaux retenus (« 4G », « 5G »).
    network: list[str] | None = None
    # kind : type de forfait (tous, volume limité, illimité).
    kind: Kind = "all"
    # min_price / max_price : bornes de prix en euros, incluses.
    min_price: float | None = None
    max_price: float | None = None
    # q : texte cherché dans le fournisseur, le nom d'offre, la destination et le réseau.
    q: str | None = None
