/**
 * Ouvre le résumé d'un volume de data (clic sur le graphique « Prix selon le volume »).
 * @param {Object} point point Plotly cliqué ; customdata[1] = volume en Go ou « unlimited »
 */
function volumeSummary(point) {
  const key = point.customdata[1];
  const unlimited = key === "unlimited";
  openSummary({
    kind: "Volume de data", title: unlimited ? "Forfaits illimités" : point.x, groupBy: "provider",
    rows: current.filter(o => unlimited ? o.unlimited : o.gb === key),
    list: { search: unlimited ? "illimité" : `data=${key}go` },
  });
}
