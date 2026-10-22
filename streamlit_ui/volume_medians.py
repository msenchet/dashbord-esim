"""Prix médian par volume de data."""
import pandas as pd


def volume_medians(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule le prix médian et le nombre d'offres pour chaque volume (« 5 Go », « Illimité »).

    Args:
        df: offres retenues par les filtres.

    Returns:
        Un tableau (volume, order, median, count) trié du plus petit volume à l'illimité.
    """
    # volume : libellé du volume ; order : clé de tri (l'illimité est placé en dernier).
    labelled = df.assign(
        volume=df["data_gb"].map(lambda gb: f"{gb:g} Go").where(~df["is_unlimited"], "Illimité"),
        order=df["data_gb"].fillna(1e9))
    return (labelled.groupby(["volume", "order"], as_index=False)["price"]
            .agg(["median", "count"]).sort_values("order"))
