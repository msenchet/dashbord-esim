/**
 * Compare deux nombres avec un opérateur de la recherche.
 * @param {string} op « < », « <= », « > », « >= » ou « = »
 * @param {number} value valeur de l'offre
 * @param {number} limit valeur tapée dans la recherche
 * @returns {boolean} résultat de la comparaison
 */
function compareValues(op, value, limit) {
  switch (op) {
    case "<": return value < limit;
    case "<=": return value <= limit;
    case ">": return value > limit;
    case ">=": return value >= limit;
    default: return Math.abs(value - limit) < 1e-9;
  }
}
