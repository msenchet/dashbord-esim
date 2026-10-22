/**
 * Cellule « €/Go » teintée : bleu sous la moyenne, rouge au-dessus, intensité selon l'écart.
 * @param {Object} offer offre
 * @param {number} avg prix moyen au Go des offres affichées
 * @returns {string} HTML de la cellule (« — » si le prix au Go est inconnu)
 */
function perGbCell(offer, avg) {
  if (offer.perGb === null) return "—";
  // d : écart relatif à la moyenne, entre -1 et 1 ; strength : opacité de la teinte en %.
  const d = Math.max(-1, Math.min(1, (offer.perGb - avg) / avg));
  const pole = d < 0 ? "var(--c-blue)" : "var(--c-red)";
  const strength = Math.round(8 + 30 * Math.abs(d));
  const background = `color-mix(in srgb, ${pole} ${strength}%, transparent)`;
  return `<span class="tint" style="background: ${background}"
    title="${d < 0 ? "Moins cher" : "Plus cher"} que la moyenne (${fmtEur(avg)}/Go)">`
    + `${fmtEur(offer.perGb)}</span>`;
}
