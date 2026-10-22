/**
 * Ouvre le résumé d'une tranche de prix (clic sur une barre de l'histogramme).
 * @param {Object} point point Plotly cliqué ; customdata = [début, fin, infobulle]
 */
function priceBandSummary(point) {
  const [low, high] = point.customdata;
  openSummary({
    kind: "Tranche de prix", title: `${fmtEur(low, 0)} – ${fmtEur(high, 0)}`, groupBy: "provider",
    rows: current.filter(o => o.price >= low && o.price < high),
    list: { search: `prix>=${low} prix<${high}` },
  });
}
