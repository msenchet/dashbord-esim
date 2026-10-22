"""Route POST /api/import/url : import depuis une URL."""
import httpx
from fastapi import HTTPException

from esim import read_any

from .config import MAX_IMPORT_BYTES, URL_TIMEOUT_SECONDS
from .merge_offers import merge_offers
from .models import UrlImport
from .parse_import import parse_import


def import_url(body: UrlImport) -> dict:
    """Télécharge une API JSON ou un fichier CSV en ligne puis importe son contenu.

    Args:
        body: URL à télécharger et mode d'import.

    Returns:
        Le bilan de l'import (voir merge_offers).

    Raises:
        HTTPException: 502 si l'URL est injoignable, 413 si la réponse dépasse 20 Mo,
            422 si le contenu est illisible.
    """
    try:
        resp = httpx.get(str(body.url), timeout=URL_TIMEOUT_SECONDS, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(502, f"Impossible de récupérer {body.url} : {exc}") from exc
    if len(resp.content) > MAX_IMPORT_BYTES:
        raise HTTPException(413, "Réponse supérieure à 20 Mo")
    # name : nom de fichier déduit de l'URL ; « .json » ajouté si le serveur annonce du JSON.
    name = body.url.path.rsplit("/", 1)[-1] if body.url.path else body.url.host
    if "json" in resp.headers.get("content-type", "") and not name.endswith(".json"):
        name += ".json"
    try:
        df = read_any(resp.content, name or "import")
    except Exception as exc:
        raise HTTPException(422, f"Contenu illisible : {exc}") from exc
    return merge_offers(parse_import([(df, name or str(body.url))]), body.mode, str(body.url))
