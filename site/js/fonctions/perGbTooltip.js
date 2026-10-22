/**
 * Texte de l'infobulle d'un fournisseur dans le graphique « Prix moyen au Go ».
 * @param {Object} p ligne du fournisseur (voir byProvider)
 * @param {number} avg prix moyen au Go de toutes les offres affichées
 * @returns {string} texte HTML de l'infobulle
 */
function perGbTooltip(p, avg) {
  const d = p.perGb - avg;
  const gap = Math.abs(d) < 0.005 ? "dans la moyenne"
    : `${fmtEur(Math.abs(d))} ${d < 0 ? "de moins" : "de plus"} que la moyenne (${fmtEur(avg)}/Go)`;
  return `${fmtEur(p.perGb)}/Go<br>${gap}<br>`
    + `${fmtInt(p.count)} offres dont ${fmtInt(p.unlimited)} illimitées`;
}
