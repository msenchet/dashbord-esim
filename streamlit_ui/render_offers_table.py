"""Tableau « Toutes les offres »."""
import pandas as pd
import streamlit as st

from .config import OFFER_COLUMNS


def render_offers_table(table: pd.DataFrame) -> None:
    """Affiche les offres triées par prix, avec des colonnes formatées.

    Args:
        table: offres à afficher (après filtres et recherche).
    """
    st.dataframe(
        table[OFFER_COLUMNS].sort_values("price"),
        hide_index=True, width="stretch", height=420,
        column_config={
            "provider": "Fournisseur", "product_name": "Offre", "country_name": "Destination",
            "data_display": "Data",
            "validity_days": st.column_config.NumberColumn("Validité", format="%d j"),
            "price": st.column_config.NumberColumn("Prix", format="%.2f €"),
            "price_per_gb": st.column_config.NumberColumn("€/Go", format="%.2f €"),
            "network": "Réseau",
            "top_up": st.column_config.CheckboxColumn("Recharge"),
        },
    )
