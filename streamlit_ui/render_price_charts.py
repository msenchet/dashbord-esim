"""Graphiques des prix (distribution et prix médian par volume)."""
import pandas as pd
import plotly.express as px
import streamlit as st

from esim import EXPENSIVE_THRESHOLD

from .config import BLUE, GRAY, HIST_BINS
from .style_figure import style_figure
from .volume_medians import volume_medians


def render_price_charts(df: pd.DataFrame) -> None:
    """Affiche côte à côte l'histogramme des prix et le prix médian selon le volume.

    Args:
        df: offres retenues par les filtres.
    """
    left, right = st.columns(2)
    with left:
        st.subheader("Distribution des prix")
        fig = px.histogram(df, x="price", nbins=HIST_BINS, labels={"price": "Prix (€)"})
        fig.update_traces(marker_color=BLUE, hovertemplate="%{x} €<br>%{y} offres<extra></extra>")
        fig.add_vline(x=EXPENSIVE_THRESHOLD, line_dash="dot", line_color=GRAY,
                      annotation_text="100 €", annotation_position="top")
        fig.update_yaxes(title="Offres")
        st.plotly_chart(style_figure(fig), width="stretch")
    with right:
        st.subheader("Prix médian selon le volume de data")
        fig = px.bar(volume_medians(df), x="volume", y="median", custom_data=["count"],
                     labels={"volume": "Volume", "median": "Prix médian (€)"})
        fig.update_traces(marker_color=BLUE,
                          hovertemplate="<b>%{x}</b><br>Prix médian : %{y:.2f} €"
                                        "<br>%{customdata[0]} offres<extra></extra>")
        fig.update_xaxes(type="category")
        st.plotly_chart(style_figure(fig), width="stretch")
