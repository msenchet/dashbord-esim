"""Contrôle de la clé API sur les routes d'écriture."""
import os

from fastapi import Header, HTTPException

from .config import API_KEY_ENV


def require_key(x_api_key: str | None = Header(default=None)) -> None:
    """Refuse la requête si une clé API est configurée et que l'en-tête X-API-Key ne correspond pas.

    Sans variable d'environnement ESIM_API_KEY, toutes les requêtes sont acceptées.

    Args:
        x_api_key: valeur de l'en-tête HTTP « X-API-Key » envoyé par le client.

    Raises:
        HTTPException: 401 si la clé est absente ou fausse.
    """
    # expected : clé attendue, lue à chaque requête pour pouvoir la changer sans redémarrer.
    expected = os.environ.get(API_KEY_ENV)
    if expected and x_api_key != expected:
        raise HTTPException(401, "Clé API invalide ou manquante (en-tête X-API-Key)")
