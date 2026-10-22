/**
 * Renvoie « s » si le nombre demande un pluriel en français (au-delà de 1).
 * @param {number} count nombre d'éléments
 * @returns {string} « s » ou chaîne vide
 */
function plural(count) {
  return count > 1 ? "s" : "";
}
