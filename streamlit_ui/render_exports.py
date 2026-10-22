"""Boutons de téléchargement des offres affichées."""
import json

import pandas as pd
import streamlit as st

from esim import compute_stats, csv_safe, to_records


def render_exports(table: pd.DataFrame) -> None:
    """Propose le téléchargement des offres affichées en CSV et en JSON (format de l'API).

    Args:
        table: offres affichées (après filtres et recherche).
    """
    # records : offres au format de l'API ; stats : indicateurs, NaN remplacés par null.
    records = to_records(table)
    stats = {key: None if pd.isna(value) else float(value)
             for key, value in compute_stats(table).items()}
    export = st.columns(2)
    export[0].download_button("Télécharger les offres filtrées (CSV)",
                              csv_safe(pd.DataFrame(records)).to_csv(index=False)
                              .encode("utf-8-sig"),
                              file_name="offres_esim_filtrees.csv", mime="text/csv")
    export[1].download_button("Télécharger les offres filtrées (JSON)",
                              json.dumps({"total": len(table), "stats": stats, "offers": records},
                                         ensure_ascii=False, indent=1),
                              file_name="offres_esim_filtrees.json", mime="application/json")
