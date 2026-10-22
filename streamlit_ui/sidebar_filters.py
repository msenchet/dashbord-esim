"""Section « Filtres » de la barre latérale."""
import math

import pandas as pd
import streamlit as st

from .config import KIND_CHOICES


def sidebar_filters(offers: pd.DataFrame) -> dict:
    """Affiche les filtres (fournisseurs, destinations, validité, réseau, prix, forfait).

    Args:
        offers: offres chargées, pour proposer les valeurs existantes.

    Returns:
        Les choix de l'utilisateur : providers, countries, validities, networks (listes,
        vides = pas de filtre), price_range (couple min, max) et kind (type de forfait).
    """
    with st.sidebar:
        st.header("Filtres")
        providers = st.multiselect("Fournisseurs", sorted(offers["provider"].unique()),
                                   placeholder="Tous les fournisseurs")
        countries = st.multiselect("Destinations", sorted(offers["country_name"].unique()),
                                   placeholder="Toutes les destinations")
        validities = st.multiselect("Validité (jours)",
                                    sorted(offers["validity_days"].dropna().unique()),
                                    placeholder="Toutes les durées")
        networks = st.multiselect("Réseau", sorted(offers["network"].unique()),
                                  placeholder="4G et 5G")
        # low / high : bornes du curseur, arrondies à l'euro.
        low = float(math.floor(offers["price"].min()))
        high = float(math.ceil(offers["price"].max()))
        price_range = st.slider("Prix (€)", low, high, (low, high), step=1.0)
        kind = st.radio("Type de forfait", KIND_CHOICES, horizontal=True)
    return {"providers": providers, "countries": countries, "validities": validities,
            "networks": networks, "price_range": price_range, "kind": kind}
