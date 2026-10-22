"""Route GET /api/offers.csv : export CSV des offres."""
import pandas as pd
from fastapi import Depends
from fastapi.responses import Response

from esim import EXPORT_COLUMNS, csv_safe, to_records

from . import store
from .apply_filters import apply_filters
from .get_filters import get_filters
from .models import OfferFilters


def get_offers_csv(filters: OfferFilters = Depends(get_filters)) -> Response:
    """Renvoie les offres filtrées en fichier CSV, triées par prix croissant.

    Le fichier commence par un BOM UTF-8 pour qu'Excel affiche correctement les accents ;
    les textes qui ressemblent à une formule sont neutralisés (voir esim.csv_safe).

    Args:
        filters: filtres lus dans l'URL.

    Returns:
        Une réponse « text/csv » à télécharger sous le nom offres_esim.csv.
    """
    # df : offres filtrées ; csv : leur contenu CSV, en-tête inclus même s'il n'y a aucune offre.
    df = apply_filters(store.offers, filters).sort_values("price")
    csv = csv_safe(pd.DataFrame(to_records(df), columns=EXPORT_COLUMNS)).to_csv(index=False)
    return Response("﻿" + csv, media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": 'attachment; filename="offres_esim.csv"'})
