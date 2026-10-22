"""Nom de fournisseur déduit d'un nom de fichier."""
from pathlib import Path


def provider_from_filename(path: Path) -> str:
    """Transforme un nom de fichier en nom de fournisseur : « super_sim.csv » → « Super Sim ».

    Sert quand un fichier importé n'a pas de colonne « provider ».

    Args:
        path: chemin (ou simple nom) du fichier source.

    Returns:
        Le nom du fournisseur, chaque mot commençant par une majuscule.
    """
    return path.stem.replace("_", " ").replace("-", " ").strip().title()
