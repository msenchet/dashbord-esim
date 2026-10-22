/**
 * Ligne d'offre du résumé (nom, fournisseur si utile, prix).
 * @param {Object} o offre
 * @param {string} value prix formaté affiché à droite
 * @param {string} groupBy « country » (résumé d'un fournisseur) ou « provider »
 * @returns {string} HTML de la ligne
 */
function summaryOfferLine(o, value, groupBy) {
  const provider = groupBy === "provider" ? ` · <b>${esc(o.provider)}</b>` : "";
  return `<li><span class="o-name">${esc(o.name)}${provider}</span>
    <span class="o-price">${value}</span></li>`;
}
