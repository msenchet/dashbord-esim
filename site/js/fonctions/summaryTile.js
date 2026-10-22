/**
 * Petite carte chiffrée du résumé.
 * @param {string} label libellé
 * @param {string} value valeur formatée
 * @param {string} [extra=""] HTML ajouté sous la valeur
 * @returns {string} HTML de la carte
 */
function summaryTile(label, value, extra = "") {
  return `<div class="sum-tile"><div class="label">${label}</div>`
    + `<div class="value">${value}</div>${extra}</div>`;
}
