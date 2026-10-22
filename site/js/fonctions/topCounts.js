/**
 * Valeurs les plus fréquentes d'un champ (destinations ou fournisseurs principaux).
 * @param {Object[]} rows offres
 * @param {string} key champ compté
 * @param {number} [n=TOP_N] nombre de valeurs gardées
 * @returns {Array} couples [valeur, nombre], du plus fréquent au moins fréquent
 */
function topCounts(rows, key, n = TOP_N) {
  const counts = new Map();
  rows.forEach(o => counts.set(o[key], (counts.get(o[key]) || 0) + 1));
  return [...counts].sort((a, b) => b[1] - a[1]).slice(0, n);
}
