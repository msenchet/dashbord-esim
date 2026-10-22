/**
 * Mise en page Plotly commune (fond transparent, couleurs du thème, virgule décimale).
 * @param {Object} [extra] réglages propres au graphique, qui remplacent ceux par défaut
 * @returns {Object} mise en page complète
 */
function baseLayout(extra = {}) {
  return Object.assign({
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
      color: css("--text-2"), size: 13 },
    margin: { l: 8, r: 16, t: 8, b: 8 },
    bargap: 0.25,
    showlegend: false,
    separators: ", ",
    hoverlabel: { bgcolor: css("--surface"), bordercolor: css("--border"),
      font: { color: css("--text"), size: 13 } },
    xaxis: { gridcolor: css("--grid"), zeroline: false, automargin: true, fixedrange: true },
    yaxis: { gridcolor: css("--grid"), zeroline: false, automargin: true, fixedrange: true },
  }, extra);
}
