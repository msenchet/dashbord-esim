"""Lecture d'un CSV quel que soit son séparateur."""
import pandas as pd


def read_csv_any_separator(source) -> pd.DataFrame:
    """Lit un CSV séparé par « , » ou « ; » (détection automatique) en gardant tout en texte.

    Args:
        source: chemin du fichier ou flux texte (io.StringIO).

    Returns:
        Le tableau brut, toutes les colonnes en texte.
    """
    # sep=None + moteur « python » : pandas devine le séparateur à partir des premières lignes.
    return pd.read_csv(source, sep=None, engine="python", dtype=str,
                       encoding="utf-8-sig", skip_blank_lines=True)
