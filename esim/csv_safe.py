"""Protection des exports CSV contre l'injection de formules."""
import pandas as pd

from .config import CSV_FORMULA_CHARS


def csv_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Neutralise les textes qu'Excel exécuterait comme une formule (« =HYPERLINK(…) »).

    Une apostrophe est ajoutée devant chaque texte commençant par = + - @, tabulation ou
    retour chariot : le tableur l'affiche alors comme du texte. Les nombres ne changent pas.

    Args:
        df: tableau à exporter.

    Returns:
        Une copie du tableau, prête à être écrite en CSV.
    """
    safe = df.copy()
    for col in safe.columns:
        if safe[col].dtype == object or pd.api.types.is_string_dtype(safe[col]):
            safe[col] = safe[col].map(
                lambda v: "'" + v if isinstance(v, str) and v.startswith(CSV_FORMULA_CHARS) else v)
    return safe
