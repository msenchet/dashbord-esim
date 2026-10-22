/**
 * Indique si une valeur est actuellement sélectionnée par clic.
 * @param {string} field colonne
 * @param {string} value valeur texte
 * @returns {boolean} true si elle filtre la liste
 */
function isPicked(field, value) {
  return !!state.picks[field]?.has(value);
}
