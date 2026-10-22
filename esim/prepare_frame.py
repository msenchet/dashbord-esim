"""Harmonisation des colonnes d'une source avant nettoyage."""
from pathlib import Path

import pandas as pd

from .normalize_column import normalize_column
from .provider_from_filename import provider_from_filename


def prepare_frame(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """Renomme les colonnes d'une source et complète le fournisseur manquant.

    Args:
        df: tableau brut lu depuis un fichier ou une API.
        source_name: nom du fichier source (sert de fournisseur par défaut et de traçabilité).

    Returns:
        Une copie du tableau avec les noms de colonnes internes, une colonne « provider »
        toujours remplie et une colonne « source_file ».
    """
    df = df.copy()
    df.columns = [normalize_column(c) for c in df.columns]
    # Deux colonnes peuvent devenir identiques après normalisation : on garde la première.
    df = df.loc[:, ~df.columns.duplicated()]
    # fallback : fournisseur déduit du nom de fichier, utilisé quand la colonne est vide.
    fallback = provider_from_filename(Path(source_name))
    if "provider" not in df.columns:
        df["provider"] = fallback
    df["provider"] = (df["provider"].astype("string").str.strip()
                      .replace("", pd.NA).fillna(fallback))
    df["source_file"] = source_name
    return df
