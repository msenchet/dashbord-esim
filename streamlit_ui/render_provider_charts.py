"""Graphiques par fournisseur (nombre d'offres et prix au Go)."""
import pandas as pd
import plotly.express as px
import streamlit as st

from .config import BLUE, TALL_CHART
from .style_figure import style_figure


def render_provider_charts(breakdown: pd.DataFrame) -> None:
    """Affiche côte à côte le nombre d'offres et le prix moyen au Go par fournisseur.

    Args:
        breakdown: répartition par fournisseur (esim.provider_breakdown, index remis en colonne).
    """
    left, right = st.columns(2)
    with left:
        st.subheader("Nombre d'offres par fournisseur")
        fig = px.bar(breakdown.sort_values("offres"), x="offres", y="provider", orientation="h",
                     custom_data=["part_%", "prix_moyen"],
                     labels={"offres": "Offres", "provider": ""})
        fig.update_traces(marker_color=BLUE,
                          hovertemplate="<b>%{y}</b><br>%{x} offres (%{customdata[0]:.1f} %)"
                                        "<br>Prix moyen : %{customdata[1]:.2f} €<extra></extra>")
        st.plotly_chart(style_figure(fig, TALL_CHART), width="stretch")
    with right:
        st.subheader("Prix moyen au Go par fournisseur")
        # per_gb : fournisseurs ayant un prix au Go, du plus cher au moins cher.
        per_gb = (breakdown.dropna(subset=["prix_moyen_par_go"])
                  .sort_values("prix_moyen_par_go", ascending=False))
        fig = px.bar(per_gb, x="prix_moyen_par_go", y="provider", orientation="h",
                     custom_data=["offres", "offres_illimitees"],
                     labels={"prix_moyen_par_go": "€/Go (hors illimité)", "provider": ""})
        fig.update_traces(marker_color=BLUE,
                          hovertemplate="<b>%{y}</b><br>%{x:.2f} €/Go<br>%{customdata[0]} offres "
                                        "dont %{customdata[1]} illimitées<extra></extra>")
        st.plotly_chart(style_figure(fig, TALL_CHART), width="stretch")
        st.caption("Plus la barre est courte, moins le Go est cher. Forfaits illimités exclus.")
