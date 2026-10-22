/**
 * Pourcentage arrondi : pct(1, 4) → « 25 % ».
 * @param {number} part effectif de la partie
 * @param {number} total effectif total
 * @returns {string} pourcentage formaté, « — » si le total est nul
 */
function pct(part, total) {
  return total ? Math.round(part / total * 100) + " %" : "—";
}
