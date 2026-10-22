/**
 * Moyenne d'une liste de nombres.
 * @param {number[]} values nombres
 * @returns {number} la moyenne, NaN si la liste est vide
 */
function mean(values) {
  return values.length ? values.reduce((sum, x) => sum + x, 0) / values.length : NaN;
}
