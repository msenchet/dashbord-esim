"""Tableau « Répartition par fournisseur »."""
import pandas as pd
import streamlit as st


def render_breakdown_table(breakdown: pd.DataFrame) -> None:
    """Affiche la répartition par fournisseur avec des colonnes formatées (%, €).

    Args:
        breakdown: répartition par fournisseur (esim.provider_breakdown, index remis en colonne).
    """
    st.subheader("Répartition par fournisseur")
    st.dataframe(
        breakdown,
        hide_index=True, width="stretch",
        column_config={
            "provider": "Fournisseur",
            "offres": "Offres",
            "part_%": st.column_config.NumberColumn("Part", format="%.1f %%"),
            "prix_moyen": st.column_config.NumberColumn("Prix moyen", format="%.2f €"),
            "prix_min": st.column_config.NumberColumn("Prix min", format="%.2f €"),
            "prix_max": st.column_config.NumberColumn("Prix max", format="%.2f €"),
            "offres_illimitees": "Illimitées",
            "prix_moyen_par_go": st.column_config.NumberColumn("€/Go", format="%.2f €"),
        },
    )
