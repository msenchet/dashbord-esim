/**
 * Dessine « Prix moyen au Go par fournisseur » : bleu sous la moyenne, rouge au-dessus,
 * avec une ligne pointillée sur la moyenne.
 * @param {Object[]} rows offres affichées
 * @param {Object[]} prov lignes par fournisseur (voir byProvider)
 */
function renderPerGbChart(rows, prov) {
  // pg : fournisseurs avec un prix au Go, du plus cher au moins cher ; avg : moyenne globale.
  const pg = prov.filter(p => p.perGb !== null).sort((a, b) => b.perGb - a.perGb);
  const avg = computeStats(rows).price_per_gb_mean;
  const spread = Math.max(...pg.map(p => Math.abs(p.perGb - avg)), 0);
  const trace = withColors({
    type: "bar", orientation: "h", x: pg.map(p => p.perGb), y: pg.map(p => p.provider),
    customdata: pg.map(p => [p.count, p.unlimited, perGbTooltip(p, avg)]),
    hovertemplate: "<b>%{y}</b><br>%{customdata[2]}" + CLICK_HINT,
  }, pg.map(p => divergingColor(p.perGb, avg, spread)));
  // Ligne et étiquette de la moyenne, seulement si elle existe (pas d'offre illimitée seule).
  const hasMean = avg !== null;
  const meanLine = hasMean ? [{ type: "line", x0: avg, x1: avg, yref: "paper", y0: 0, y1: 1,
    line: { color: css("--ref"), dash: "dot", width: 1.5 } }] : [];
  const meanLabel = hasMean ? [{ x: avg, yref: "paper", y: 1, yanchor: "bottom",
    text: "moy. " + fmtEur(avg), showarrow: false,
    font: { color: css("--text-2"), size: 12 } }] : [];
  Plotly.react("c-pergb", [trace], baseLayout({
    xaxis: { ...baseLayout().xaxis, title: { text: "€/Go (hors illimité)" } },
    yaxis: { ...baseLayout().yaxis, showgrid: false },
    shapes: meanLine,
    annotations: meanLabel,
    margin: { l: 8, r: 16, t: 22, b: 8 },
  }), PLOT_CONFIG);
}
