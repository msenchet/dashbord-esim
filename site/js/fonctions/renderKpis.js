/**
 * Affiche les cartes d'indicateurs (KPI) en haut de page.
 * Chaque carte : [libellé, valeur, aide, classe de couleur, icône].
 * @param {Object[]} rows offres retenues par les filtres
 */
function renderKpis(rows) {
  const s = computeStats(rows);
  const dataMean = s.data_mean_gb === null ? "—"
    : s.data_mean_gb.toLocaleString("fr-FR", { maximumFractionDigits: 1 }) + " Go";
  const perGb = s.price_per_gb_mean === null ? "—" : fmtEur(s.price_per_gb_mean) + "/Go";
  const cards = [
    ["Cartes eSIM", fmtInt(s.total_offers), "Offres après filtres", "c-blue", "#"],
    [`Offres > ${THRESHOLD} €`, fmtInt(s.offers_over_100), "Prix supérieur à 100 €",
      "c-orange", "!"],
    ["Prix minimum", fmtEur(s.price_min), "", "c-orange", "↓"],
    ["Prix maximum", fmtEur(s.price_max), "", "c-orange", "↑"],
    ["Prix moyen", fmtEur(s.price_mean), "", "c-orange", "€"],
    ["Data moyenne / carte", dataMean, "Hors forfaits illimités", "c-aqua", "Go"],
    ["Prix moyen au Go", perGb, "Hors forfaits illimités", "c-aqua", "÷"],
    ["Forfaits illimités", fmtInt(s.unlimited_offers), "Exclus des moyennes data", "c-violet", "∞"],
    ["Fournisseurs", fmtInt(s.providers), "", "c-magenta", "◆"],
  ];
  document.getElementById("kpis").innerHTML = cards.map(([label, value, hint, color, icon]) =>
    `<div class="kpi ${color}"><div class="label">
        <span class="icon" aria-hidden="true">${icon}</span>${label}</div>
      <div class="value">${value}</div><div class="hint">${hint || "&nbsp;"}</div></div>`).join("");
}
