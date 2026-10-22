"""Route POST /api/import/url : import depuis une URL publique."""
import httpx
from fastapi import HTTPException

from esim import fetch_public_url, read_any

from .config import URL_TIMEOUT_SECONDS
from .merge_offers import merge_offers
from .models import UrlImport
from .parse_import import parse_import


def import_url(body: UrlImport) -> dict:
    """Télécharge une API JSON ou un fichier CSV en ligne puis importe son contenu.

    Seules les adresses publiques sont acceptées, redirections comprises (protection SSRF),
    et la réponse est limitée à 20 Mo.

    Args:
        body: URL à télécharger et mode d'import.

    Returns:
        Le bilan de l'import (voir merge_offers).

    Raises:
        HTTPException: 400 si l'adresse est refusée ou la réponse trop grosse,
            502 si l'URL est injoignable, 422 si le contenu est illisible.
    """
    try:
        final_url, content_type, content = fetch_public_url(str(body.url), URL_TIMEOUT_SECONDS)
    except ValueError as exc:
        raise HTTPException(400, f"URL refusée : {exc}") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(502, f"Impossible de récupérer {body.url}") from exc
    # name : nom de fichier déduit de l'URL ; « .json » ajouté si le serveur annonce du JSON.
    name = final_url.split("?")[0].rstrip("/").rsplit("/", 1)[-1] or "import"
    if "json" in content_type and not name.endswith(".json"):
        name += ".json"
    try:
        df = read_any(content, name)
    except Exception as exc:
        raise HTTPException(422, "Contenu illisible (CSV ou JSON attendu)") from exc
    return merge_offers(parse_import([(df, name)]), body.mode, str(body.url))
