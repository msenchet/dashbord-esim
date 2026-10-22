/**
 * Trie des valeurs dans l'ordre alphabétique français (accents compris).
 * @param {Array} values valeurs à trier
 * @returns {Array} nouvelle liste triée
 */
function sortFr(values) {
  return [...values].sort((x, y) => String(x).localeCompare(String(y), "fr"));
}
