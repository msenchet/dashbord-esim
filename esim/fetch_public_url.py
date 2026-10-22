"""Téléchargement sécurisé d'une URL d'import."""
from urllib.parse import urljoin

import httpx

from .assert_public_url import assert_public_url
from .config import MAX_IMPORT_BYTES, MAX_REDIRECTS


def fetch_public_url(url: str, timeout: float) -> tuple[str, str, bytes]:
    """Télécharge une URL publique en contrôlant chaque redirection et la taille de la réponse.

    Les redirections sont suivies à la main (au plus MAX_REDIRECTS) pour vérifier que chaque
    nouvelle adresse est publique ; la lecture s'arrête dès que MAX_IMPORT_BYTES est dépassé.

    Args:
        url: adresse à télécharger.
        timeout: délai maximal de chaque requête, en secondes.

    Returns:
        L'URL finale (après redirections), le type de contenu annoncé et le contenu brut.

    Raises:
        ValueError: adresse refusée, trop de redirections ou réponse trop volumineuse.
        httpx.HTTPError: serveur injoignable ou réponse en erreur.
    """
    for _ in range(MAX_REDIRECTS + 1):
        assert_public_url(url)
        with httpx.stream("GET", url, timeout=timeout, follow_redirects=False) as resp:
            if resp.is_redirect:
                url = urljoin(url, resp.headers.get("location", ""))
                continue
            resp.raise_for_status()
            # chunks : morceaux lus ; size : octets déjà reçus.
            chunks, size = [], 0
            for chunk in resp.iter_bytes():
                size += len(chunk)
                if size > MAX_IMPORT_BYTES:
                    raise ValueError("réponse supérieure à 20 Mo")
                chunks.append(chunk)
            return url, resp.headers.get("content-type", ""), b"".join(chunks)
    raise ValueError(f"plus de {MAX_REDIRECTS} redirections")
