"""Conversion d'un contenu JSON importé en tableau d'offres."""
import pandas as pd


def records_from_json(payload) -> pd.DataFrame:
    """Accepte une liste d'offres ou un objet ``{"offers": [...]}`` / ``{"data": [...]}``.

    Le format ``{"offers": [...]}`` est celui renvoyé par l'API du projet.

    Args:
        payload: contenu JSON déjà décodé (liste ou dictionnaire).

    Returns:
        Le tableau brut des offres.

    Raises:
        ValueError: si aucune liste d'offres n'est trouvée.
    """
    if isinstance(payload, dict):
        payload = payload.get("offers", payload.get("data", payload.get("items")))
    if not isinstance(payload, list):
        raise ValueError("JSON attendu : une liste d'offres ou un objet {\"offers\": [...]}")
    return pd.DataFrame(payload)
