"""Cartes d'indicateurs (KPI)."""
import streamlit as st

from esim import EXPENSIVE_THRESHOLD

from .euro import euro


def render_kpis(stats: dict) -> None:
    """Affiche les 9 indicateurs sur trois lignes de trois cartes.

    La data moyenne et le prix au Go valent « — » quand toutes les offres sont illimitées.

    Args:
        stats: indicateurs calculés par esim.compute_stats.
    """
    # has_limited : au moins une offre à volume fini (sinon les moyennes de data n'existent pas).
    has_limited = stats["unlimited_offers"] < stats["total_offers"]
    row1 = st.columns(3)
    row1[0].metric("Cartes eSIM", f"{stats['total_offers']:,}".replace(",", " "),
                   help="Nombre total d'offres après filtres")
    row1[1].metric(f"Offres > {EXPENSIVE_THRESHOLD:.0f} €", stats["offers_over_100"],
                   help="Offres dont le prix dépasse 100 €")
    row1[2].metric("Prix moyen au Go",
                   euro(stats["price_per_gb_mean"]) + "/Go" if has_limited else "—",
                   help="Moyenne du prix/Go de chaque offre, hors forfaits illimités")
    row2 = st.columns(3)
    row2[0].metric("Prix minimum", euro(stats["price_min"]))
    row2[1].metric("Prix maximum", euro(stats["price_max"]))
    row2[2].metric("Prix moyen", euro(stats["price_mean"]))
    row3 = st.columns(3)
    row3[0].metric("Data moyenne par carte",
                   f"{stats['data_mean_gb']:.1f} Go".replace(".", ",") if has_limited else "—",
                   help="Calculée uniquement sur les forfaits à volume fini")
    row3[1].metric("Forfaits illimités", stats["unlimited_offers"],
                   help="Exclus des moyennes de data et de prix/Go")
    row3[2].metric("Fournisseurs", stats["providers"])
