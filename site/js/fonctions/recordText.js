/**
 * Lit un champ texte d'une ligne importée.
 * @param {Object} record ligne normalisée
 * @param {string} key nom interne du champ
 * @returns {string|null} texte sans espaces autour, null si vide
 */
function recordText(record, key) {
  return isBlank(record[key]) ? null : String(record[key]).trim();
}
