"""Mise en forme commune des graphiques Plotly."""
from .config import CHART_HEIGHT


def style_figure(fig, height: int = CHART_HEIGHT):
    """Applique la mise en page commune : marges fines, pas de légende, grille discrète.

    Args:
        fig: figure Plotly à mettre en forme (modifiée).
        height: hauteur en pixels.

    Returns:
        La même figure.
    """
    fig.update_layout(height=height, margin=dict(l=8, r=8, t=8, b=8), bargap=0.25,
                      hoverlabel=dict(font_size=13), showlegend=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridwidth=1, zeroline=False)
    return fig
