/**
 * Médiane d'une liste de nombres (valeur du milieu une fois triée).
 * @param {number[]} values nombres
 * @returns {number} la médiane, NaN si la liste est vide
 */
function median(values) {
  if (!values.length) return NaN;
  // sorted : copie triée ; middle : index du milieu.
  const sorted = [...values].sort((x, y) => x - y);
  const middle = sorted.length >> 1;
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}
