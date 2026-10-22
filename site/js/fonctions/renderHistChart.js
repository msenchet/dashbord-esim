/**
 * Dessine « Distribution des prix » par tranches de HIST_STEP euros ; > 100 € en orange.
 * @param {Object[]} rows offres affichées
 */
function renderHistChart(rows) {
  // bins : nombre d'offres par tranche, indexé par le prix de début de tranche.
  const bins = new Map();
  rows.forEach(o => {
    const start = Math.floor(o.price / HIST_STEP) * HIST_STEP;
    bins.set(start, (bins.get(start) || 0) + 1);
  });
  const starts = [...bins.keys()].sort((a, b) => a - b);
  const trace = withColors({
    type: "bar", x: starts.map(k => k + HIST_STEP / 2), y: starts.map(k => bins.get(k)),
    width: HIST_STEP * 0.85,
    customdata: starts.map(k => [k, k + HIST_STEP,
      `<b>${fmtEur(k, 0)} – ${fmtEur(k + HIST_STEP, 0)}</b><br>${fmtInt(bins.get(k))} offres`]),
    hovertemplate: "%{customdata[2]}" + CLICK_HINT,
  }, starts.map(k => css(k >= THRESHOLD ? "--c-orange" : "--c-blue")));
  Plotly.react("c-hist", [trace], baseLayout({
    xaxis: { ...baseLayout().xaxis, title: { text: "Prix (€)" }, showgrid: false },
    yaxis: { ...baseLayout().yaxis, title: { text: "Offres" } },
    shapes: [{ type: "line", x0: THRESHOLD, x1: THRESHOLD, yref: "paper", y0: 0, y1: 1,
      line: { color: css("--ref"), dash: "dot", width: 1.5 } }],
    annotations: [{ x: THRESHOLD, yref: "paper", y: 1, text: "100 €", showarrow: false,
      xanchor: "left", xshift: 4, font: { color: css("--text-2") } }],
  }), PLOT_CONFIG);
}
