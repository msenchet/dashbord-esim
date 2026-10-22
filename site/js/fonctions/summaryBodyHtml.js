/**
 * Contenu du panneau de résumé : prix, parts, principaux groupes et offres les moins chères.
 * @param {Object[]} rows offres de la sélection
 * @param {string} groupBy champ des « principaux » : « country » ou « provider »
 * @param {Object} s indicateurs de la sélection
 * @param {string} deltaHtml comparaison du prix au Go à la moyenne
 * @returns {string} HTML du contenu
 */
function summaryBodyHtml(rows, groupBy, s, deltaHtml) {
  // top : groupes principaux ; cheapest : offres les moins chères ; bestGb : meilleur €/Go.
  const top = topCounts(rows, groupBy);
  const topMax = top.length ? top[0][1] : 1;
  const cheapest = [...rows].sort((a, b) => a.price - b.price).slice(0, TOP_N);
  const bestGb = rows.filter(o => o.perGb !== null).sort((a, b) => a.perGb - b.perGb)[0];
  // fiveG / topUp : nombre d'offres en 5G et rechargeables.
  const fiveG = rows.filter(o => /^5g$/i.test(o.network)).length;
  const topUp = rows.filter(o => o.topUp).length;
  const bars = top.map(([name, n]) => `<div class="mini"><span>${esc(name)}</span>
      <div class="mini-bar"><i style="width:${Math.max(4, n / topMax * 100)}%"></i></div>
      <b>${fmtInt(n)}</b></div>`).join("");
  return `<div class="sum-grid">
      ${summaryTile("Prix minimum", fmtEur(s.price_min))}
      ${summaryTile("Prix moyen", fmtEur(s.price_mean))}
      ${summaryTile("Prix maximum", fmtEur(s.price_max))}
      ${summaryTile("Prix moyen au Go",
        s.price_per_gb_mean === null ? "—" : fmtEur(s.price_per_gb_mean), deltaHtml)}
    </div>
    <div class="sum-shares">
      <span><b>${pct(s.unlimited_offers, rows.length)}</b> illimitées</span>
      <span><b>${pct(fiveG, rows.length)}</b> en 5G</span>
      <span><b>${pct(topUp, rows.length)}</b> rechargeables</span>
      <span><b>${fmtInt(new Set(rows.map(o => o.country)).size)}</b> destinations</span>
    </div>
    <h3>${groupBy === "country" ? "Destinations principales" : "Fournisseurs principaux"}</h3>
    <div class="mini-bars">${bars}</div>
    <h3>Les moins chères</h3>
    <ul class="offer-list">${cheapest.map(o =>
      summaryOfferLine(o, fmtEur(o.price), groupBy)).join("")}</ul>
    ${bestGb ? `<h3>Meilleur prix au Go</h3><ul class="offer-list">`
      + `${summaryOfferLine(bestGb, fmtEur(bestGb.perGb) + "/Go", groupBy)}</ul>` : ""}`;
}
