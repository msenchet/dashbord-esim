/**
 * Ligne « x € de moins/de plus que la moyenne » sous le prix au Go du résumé.
 * @param {Object} stats indicateurs de la sélection (voir computeStats)
 * @param {Object} all indicateurs de toutes les offres affichées
 * @returns {string} HTML, vide si le prix au Go n'est pas calculable
 */
function summaryDeltaHtml(stats, all) {
  if (stats.price_per_gb_mean === null || all.price_per_gb_mean === null) return "";
  const delta = stats.price_per_gb_mean - all.price_per_gb_mean;
  return `<span class="delta">
      <i class="sw" style="--c: var(${delta < 0 ? "--c-blue" : "--c-red"})"></i>
      ${fmtEur(Math.abs(delta))} ${delta < 0 ? "de moins" : "de plus"} que la moyenne `
    + `(${fmtEur(all.price_per_gb_mean)})</span>`;
}
