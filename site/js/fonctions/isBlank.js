/**
 * Indique si une valeur importée est vide (null, undefined ou uniquement des espaces).
 * @param {*} value valeur à tester
 * @returns {boolean} true si la valeur est vide
 */
function isBlank(value) {
  return value === null || value === undefined || String(value).trim() === "";
}
