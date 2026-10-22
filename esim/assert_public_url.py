"""Contrôle qu'une URL d'import pointe vers une adresse publique (protection SSRF)."""
import ipaddress
import os
import socket
from urllib.parse import urlsplit

from .config import ALLOW_PRIVATE_URLS_ENV, ALLOWED_URL_SCHEMES


def assert_public_url(url: str) -> None:
    """Refuse une URL dont l'hôte est privé, local, réservé ou de métadonnées cloud.

    Le nom d'hôte est résolu : toutes ses adresses IP doivent être publiques. Sans ce contrôle,
    un serveur hébergé pourrait être utilisé pour lire des services internes (SSRF).
    La variable d'environnement ESIM_ALLOW_PRIVATE_URLS=1 lève la restriction (usage local).

    Args:
        url: adresse à contrôler.

    Raises:
        ValueError: si le schéma n'est pas http(s), si l'hôte est absent, introuvable
            ou s'il correspond à une adresse non publique.
    """
    parts = urlsplit(url)
    if parts.scheme not in ALLOWED_URL_SCHEMES:
        raise ValueError(f"schéma d'URL refusé : {parts.scheme or 'aucun'} (http ou https attendu)")
    if not parts.hostname:
        raise ValueError("URL sans nom d'hôte")
    if os.environ.get(ALLOW_PRIVATE_URLS_ENV) == "1":
        return
    try:
        # infos : toutes les adresses IP associées au nom d'hôte.
        infos = socket.getaddrinfo(parts.hostname, parts.port or 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"hôte introuvable : {parts.hostname}") from exc
    for info in infos:
        address = ipaddress.ip_address(info[4][0].split("%")[0])
        if not address.is_global or address.is_multicast:
            raise ValueError(f"adresse non publique refusée : {parts.hostname} ({address})")
