/**
 * Ligne HTML d'une offre dans le tableau « Toutes les offres ».
 * @param {Object} o offre
 * @param {number} avgPerGb prix moyen au Go, pour teinter la cellule €/Go
 * @returns {string} HTML de la ligne
 */
function offerRowHtml(o, avgPerGb) {
  const validity = o.validity === null ? "—" : o.validity + " j";
  const priceClass = o.price > THRESHOLD ? " price-high" : "";
  const topUp = o.topUp ? '<span class="yes">✓ Oui</span>' : '<span class="no">✕ Non</span>';
  return `<tr><td>${cellPick("provider", o, esc(o.provider))}</td><td>${esc(o.name)}</td>
    <td>${cellPick("country", o, esc(o.country))}</td>
    <td>${cellPick("display", o, esc(o.display))}</td>
    <td class="num">${cellPick("validity", o, validity)}</td>
    <td class="num${priceClass}">${fmtEur(o.price)}</td>
    <td class="num">${perGbCell(o, avgPerGb)}</td>
    <td>${cellPick("network", o, networkBadge(o.network))}</td>
    <td>${cellPick("topUp", o, topUp)}</td></tr>`;
}
