/**
 * Branche le clic des quatre graphiques sur l'ouverture du résumé correspondant.
 */
function bindChartClicks() {
  bindChartClick("c-count", point => providerSummary(point.y));
  bindChartClick("c-pergb", point => providerSummary(point.y));
  bindChartClick("c-hist", priceBandSummary);
  bindChartClick("c-volume", volumeSummary);
}
