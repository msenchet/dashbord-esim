/**
 * Dessine les quatre graphiques. Les deux graphiques par fournisseur sont masqués
 * quand un seul fournisseur est affiché (une seule barre n'apprend rien).
 * @param {Object[]} rows offres affichées
 * @param {Object[]} prov lignes par fournisseur (voir byProvider)
 */
function renderCharts(rows, prov) {
  const providerRow = document.getElementById("provider-charts");
  providerRow.hidden = prov.length < 2;
  if (!providerRow.hidden) {
    renderCountChart(prov);
    renderPerGbChart(rows, prov);
  }
  renderHistChart(rows);
  renderVolumeChart(rows);
  bindChartClicks();
}
