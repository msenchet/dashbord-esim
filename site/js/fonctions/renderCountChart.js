/**
 * Dessine « Nombre d'offres par fournisseur » : barres horizontales,
 * bleu plus foncé = plus d'offres.
 * @param {Object[]} prov lignes par fournisseur (voir byProvider)
 */
function renderCountChart(prov) {
  // asc : fournisseurs du plus petit au plus grand (Plotly dessine de bas en haut).
  const asc = [...prov].sort((a, b) => a.count - b.count);
  const maxCount = Math.max(...asc.map(p => p.count));
  const minCount = Math.min(...asc.map(p => p.count));
  const colors = asc.map(p =>
    rampColor(maxCount === minCount ? 1 : (p.count - minCount) / (maxCount - minCount)));
  const trace = withColors({
    type: "bar", orientation: "h", x: asc.map(p => p.count), y: asc.map(p => p.provider),
    customdata: asc.map(p => [p.share, p.mean,
      `${fmtInt(p.count)} offres (${p.share.toLocaleString("fr-FR", { maximumFractionDigits: 1 })}`
      + ` %)<br>Prix moyen : ${fmtEur(p.mean)}`]),
    hovertemplate: "<b>%{y}</b><br>%{customdata[2]}" + CLICK_HINT,
  }, colors);
  Plotly.react("c-count", [trace], baseLayout({
    xaxis: { ...baseLayout().xaxis, title: { text: "Offres" } },
    yaxis: { ...baseLayout().yaxis, showgrid: false },
  }), PLOT_CONFIG);
}
