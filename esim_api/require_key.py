"""Contrôle de la clé API sur les routes d'écriture."""
import os
import secrets

from fastapi import Header, HTTPException

from .config import API_KEY_ENV, OPEN_WRITE_ENV


def require_key(x_api_key: str | None = Header(default=None)) -> None:
    """Exige l'en-tête X-API-Key égal à la variable d'environnement ESIM_API_KEY.

    Sans clé configurée, l'écriture est refusée, sauf si ESIM_OPEN_WRITE=1 (développement
    local uniquement). La comparaison est faite à temps constant (secrets.compare_digest).

    Args:
        x_api_key: valeur de l'en-tête HTTP « X-API-Key » envoyé par le client.

    Raises:
        HTTPException: 403 si aucune clé n'est configurée, 401 si la clé est absente ou fausse.
    """
    # expected : clé attendue, lue à chaque requête pour pouvoir la changer sans redémarrer.
    expected = os.environ.get(API_KEY_ENV)
    if not expected:
        if os.environ.get(OPEN_WRITE_ENV) == "1":
            return
        raise HTTPException(403, "Écriture désactivée : définir ESIM_API_KEY sur le serveur "
                                 "(ou ESIM_OPEN_WRITE=1 en local)")
    if not secrets.compare_digest((x_api_key or "").encode(), expected.encode()):
        raise HTTPException(401, "Clé API invalide ou manquante (en-tête X-API-Key)")
